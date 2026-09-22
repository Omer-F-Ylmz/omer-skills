using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

namespace Jev;

public interface IJevClient
{
    Task<IReadOnlyDictionary<string, JevAnswer>> EvaluateAsync(string state, IReadOnlyDictionary<string, JevQuestion> questions, CancellationToken ct = default);

    /// <summary>State başına bir yanıt, girdi sırasıyla. ≤ChunkSize'lık parçalar, ≤MaxConcurrency eşzamanlı istek.</summary>
    Task<IReadOnlyList<IReadOnlyDictionary<string, JevAnswer>>> BatchAsync(IReadOnlyList<string> states, IReadOnlyDictionary<string, JevQuestion> questions, CancellationToken ct = default);
}

/// <summary>
/// Tek boğaz noktası: tavan (ağa çıkmadan) → TR redaksiyon (sabit, kapatılamaz) → ek redactor'lar → istek → tekrar.
/// Anahtar yalnız Authorization başlığına girer; gövde ve anahtar hiçbir hata metnine yazılmaz.
/// </summary>
public sealed class JevClient(HttpClient http, IOptions<JevOptions> options, IEnumerable<IStateRedactor> redactors) : IJevClient
{
    readonly JevOptions _o = options.Value;
    readonly IStateRedactor[] _extra = redactors.ToArray();
    int _batches, _requests;

    public int Batches => _batches;
    public int Requests => _requests;
    public Func<TimeSpan, CancellationToken, Task> Delay { get; init; } = Task.Delay;

    public async Task<IReadOnlyDictionary<string, JevAnswer>> EvaluateAsync(string state, IReadOnlyDictionary<string, JevQuestion> questions, CancellationToken ct = default) =>
        (await BatchAsync([state], questions, ct))[0];

    public async Task<IReadOnlyList<IReadOnlyDictionary<string, JevAnswer>>> BatchAsync(IReadOnlyList<string> states, IReadOnlyDictionary<string, JevQuestion> questions, CancellationToken ct = default)
    {
        var chunks = states.Chunk(_o.ChunkSize).ToList();
        if (_batches + chunks.Count > _o.MaxBatches)
            throw new JevLimitException($"batch tavanı: {chunks.Count} gerekiyor, kalan {_o.MaxBatches - _batches}");
        if (_requests + states.Count > _o.MaxRequests)
            throw new JevLimitException($"istek tavanı: en az {states.Count} gerekiyor, kalan {_o.MaxRequests - _requests}");

        using var gate = new SemaphoreSlim(_o.MaxConcurrency);
        var results = new List<IReadOnlyDictionary<string, JevAnswer>>(states.Count);
        foreach (var chunk in chunks)
        {
            Interlocked.Increment(ref _batches);
            results.AddRange(await Task.WhenAll(chunk.Select(async s =>
            {
                await gate.WaitAsync(ct);
                try { return await SendAsync(s, questions, ct); }
                finally { gate.Release(); }
            })));
        }
        return results;
    }

    async Task<IReadOnlyDictionary<string, JevAnswer>> SendAsync(string state, IReadOnlyDictionary<string, JevQuestion> questions, CancellationToken ct)
    {
        state = TurkishRedactor.Instance.Redact(state);
        foreach (var r in _extra) state = r.Redact(state);
        var request = new JevRequest(_o.Model, state, questions);
        for (var attempt = 0; ; attempt++)
        {
            if (Interlocked.Increment(ref _requests) > _o.MaxRequests)
                throw new JevLimitException($"istek tavanı: {_o.MaxRequests} HTTP isteği doldu (tekrarlar dahil)");
            using var msg = new HttpRequestMessage(HttpMethod.Post, "systemone") { Content = JsonContent.Create(request) };
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _o.ApiKey);
            using var response = await http.SendAsync(msg, ct);
            if (response.IsSuccessStatusCode)
                return (await response.Content.ReadFromJsonAsync<JevResponse>(ct))!.Answers;
            var code = (int)response.StatusCode;
            var retryable = response.StatusCode is HttpStatusCode.RequestTimeout or HttpStatusCode.TooManyRequests || code >= 500;
            if (!retryable || attempt >= _o.Retries)
                throw new HttpRequestException($"Jev {code}", null, response.StatusCode);
            await Delay(response.Headers.RetryAfter?.Delta ?? TimeSpan.FromMilliseconds(500 * Math.Pow(2, attempt)), ct);
        }
    }
}

public static class JevServiceCollectionExtensions
{
    /// <summary>appsettings "Jev" bölümü → JevOptions; typed HttpClient. ApiKey'i secret store/ortamdan verin.</summary>
    public static IServiceCollection AddJev(this IServiceCollection services, IConfiguration configuration)
    {
        services.Configure<JevOptions>(configuration.GetSection("Jev"));
        services.AddHttpClient<IJevClient, JevClient>((sp, http) =>
            http.BaseAddress = new Uri(sp.GetRequiredService<IOptions<JevOptions>>().Value.BaseUrl));
        return services;
    }
}
