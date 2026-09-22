# Jev — .NET örneği

Anahtar ortamdan okunur; gövde loglanmaz. Güven bantları SKILL.md ile aynı.

```csharp
using System.Net;
using System.Net.Http.Json;
using System.Text.Json.Serialization;

public sealed record Question(
    [property: JsonPropertyName("type")] string Type,
    [property: JsonPropertyName("instructions")] object Instructions,
    [property: JsonPropertyName("criteria")] object? Criteria = null);

public sealed record SystemOneRequest(
    [property: JsonPropertyName("model")] string Model,
    [property: JsonPropertyName("state")] object State,
    [property: JsonPropertyName("questions")] IReadOnlyDictionary<string, Question> Questions);

public sealed record Answer(
    [property: JsonPropertyName("type")] string Type,
    [property: JsonPropertyName("noul")] double? Noul,
    [property: JsonPropertyName("choice")] string? Choice,
    [property: JsonPropertyName("score")] double? Score,
    [property: JsonPropertyName("probabilities")] Dictionary<string, double>? Probabilities,
    [property: JsonPropertyName("confidence")] double? Confidence);

public sealed record Usage(
    [property: JsonPropertyName("input_tokens")] int InputTokens,
    [property: JsonPropertyName("output_tokens")] int OutputTokens);

public sealed record SystemOneResponse(
    [property: JsonPropertyName("model")] string Model,
    [property: JsonPropertyName("answers")] Dictionary<string, Answer> Answers,
    [property: JsonPropertyName("usage")] Usage Usage);

public enum Band { Act, Flag, Escalate }

public static class Confidence
{
    public static Band Of(double value) => value >= 0.85 ? Band.Act : value >= 0.60 ? Band.Flag : Band.Escalate;
}

public sealed class JevClient(HttpClient http)
{
    private static readonly HashSet<HttpStatusCode> Retryable =
        [HttpStatusCode.RequestTimeout, HttpStatusCode.TooManyRequests, (HttpStatusCode)529];

    public static HttpClient CreateHttp()
    {
        var typesafe = Environment.GetEnvironmentVariable("TYPESAFE_API_KEY");
        var key = typesafe ?? Environment.GetEnvironmentVariable("OPENROUTER_API_KEY")
            ?? throw new InvalidOperationException("TYPESAFE_API_KEY or OPENROUTER_API_KEY missing");
        var http = new HttpClient
        {
            BaseAddress = new Uri(typesafe is null ? "https://openrouter.ai/api/" : "https://api.typesafe.ai/"),
            Timeout = TimeSpan.FromSeconds(30),
        };
        http.DefaultRequestHeaders.Authorization = new("Bearer", key);
        return http;
    }

    public async Task<SystemOneResponse> EvaluateAsync(SystemOneRequest request, CancellationToken ct = default)
    {
        for (var attempt = 0; ; attempt++)
        {
            using var response = await http.PostAsJsonAsync("v1/systemone", request, ct);
            if (response.IsSuccessStatusCode)
                return (await response.Content.ReadFromJsonAsync<SystemOneResponse>(ct))!;
            var retry = Retryable.Contains(response.StatusCode) || (int)response.StatusCode >= 500;
            if (!retry || attempt == 2)
                throw new HttpRequestException($"Jev {(int)response.StatusCode}", null, response.StatusCode);
            var wait = response.Headers.RetryAfter?.Delta ?? TimeSpan.FromMilliseconds(500 * Math.Pow(2, attempt));
            await Task.Delay(wait, ct);
        }
    }
}
```

Kullanım:
```csharp
var jev = new JevClient(JevClient.CreateHttp());
var r = await jev.EvaluateAsync(new("jev-latest", new { message = "Kartımdan iki kez çekildi." },
    new Dictionary<string, Question>
    {
        ["dept"] = new("choice", "Which team should handle `message`?", new Dictionary<string, string?> { ["billing"] = null, ["technical"] = null }),
    }));
var band = Confidence.Of(r.Answers["dept"].Confidence ?? 0);
```
