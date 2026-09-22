using System.Net;
using System.Text;
using Microsoft.Extensions.Options;
using Xunit;

namespace Jev.Tests;

sealed class StubHandler(Func<int, HttpStatusCode> status, int delayMs = 0) : HttpMessageHandler
{
    int _count, _inFlight;
    public int Count => _count;
    public int MaxInFlight;
    public readonly List<string> Bodies = [];

    protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
    {
        var n = Interlocked.Increment(ref _count);
        var now = Interlocked.Increment(ref _inFlight);
        var body0 = await request.Content!.ReadAsStringAsync(ct);
        lock (Bodies)
        {
            MaxInFlight = Math.Max(MaxInFlight, now);
            Bodies.Add(body0);
        }
        try
        {
            if (delayMs > 0) await Task.Delay(delayMs, ct);
            var code = status(n);
            var body = code == HttpStatusCode.OK
                ? """{"answers":{"q":{"type":"noul","noul":0.9}}}"""
                : """{"error_type":"x"}""";
            return new HttpResponseMessage(code) { Content = new StringContent(body, Encoding.UTF8, "application/json") };
        }
        finally { Interlocked.Decrement(ref _inFlight); }
    }
}

public class JevClientTests
{
    static readonly Dictionary<string, JevQuestion> Q = new() { ["q"] = new("noul", "Acil mi?") };

    static (JevClient, StubHandler) Make(Func<int, HttpStatusCode> status, Action<JevOptions>? set = null, int delayMs = 0, IStateRedactor? extra = null)
    {
        var o = new JevOptions { ApiKey = "test" };
        set?.Invoke(o);
        var h = new StubHandler(status, delayMs);
        var http = new HttpClient(h) { BaseAddress = new Uri(o.BaseUrl) };
        var c = new JevClient(http, Options.Create(o), extra is null ? [] : [extra]) { Delay = (_, _) => Task.CompletedTask };
        return (c, h);
    }

    static List<string> States(int n) => Enumerable.Range(0, n).Select(i => $"s{i}").ToList();

    [Fact]
    public async Task Retry_5xx_then_success()
    {
        var (c, h) = Make(n => n < 3 ? HttpStatusCode.ServiceUnavailable : HttpStatusCode.OK);
        var r = await c.EvaluateAsync("x", Q, TestContext.Current.CancellationToken);
        Assert.Equal(0.9, r["q"].Noul);
        Assert.Equal(3, h.Count);
        Assert.Equal(3, c.Requests);
    }

    [Fact]
    public async Task No_retry_on_4xx()
    {
        var (c, h) = Make(_ => HttpStatusCode.BadRequest);
        await Assert.ThrowsAsync<HttpRequestException>(() => c.EvaluateAsync("x", Q, TestContext.Current.CancellationToken));
        Assert.Equal(1, h.Count);
    }

    [Fact]
    public async Task Batch_ceiling_checked_before_network()
    {
        var (c, h) = Make(_ => HttpStatusCode.OK, o => o.MaxBatches = 1);
        await Assert.ThrowsAsync<JevLimitException>(() => c.BatchAsync(States(201), Q, TestContext.Current.CancellationToken));
        Assert.Equal(0, h.Count);
    }

    [Fact]
    public async Task Request_ceiling_checked_before_network_and_counts_retries()
    {
        var (c, h) = Make(_ => HttpStatusCode.OK, o => o.MaxRequests = 2);
        await Assert.ThrowsAsync<JevLimitException>(() => c.BatchAsync(States(3), Q, TestContext.Current.CancellationToken));
        Assert.Equal(0, h.Count);

        var (c2, h2) = Make(_ => HttpStatusCode.ServiceUnavailable, o => o.MaxRequests = 2);
        await Assert.ThrowsAsync<JevLimitException>(() => c2.EvaluateAsync("x", Q, TestContext.Current.CancellationToken));
        Assert.Equal(2, h2.Count);
    }

    [Fact]
    public async Task Chunks_of_200()
    {
        var (c, h) = Make(_ => HttpStatusCode.OK, o => { o.MaxBatches = 3; o.MaxRequests = 1000; });
        var r = await c.BatchAsync(States(450), Q, TestContext.Current.CancellationToken);
        Assert.Equal(450, r.Count);
        Assert.Equal(3, c.Batches);
        Assert.Equal(450, h.Count);
    }

    [Fact]
    public async Task Concurrency_at_most_8()
    {
        var (c, h) = Make(_ => HttpStatusCode.OK, delayMs: 20);
        await c.BatchAsync(States(50), Q, TestContext.Current.CancellationToken);
        Assert.InRange(h.MaxInFlight, 2, 8);
    }

    sealed class PassThrough : IStateRedactor
    {
        public string Redact(string state) => state;
    }

    [Fact]
    public async Task Turkish_redaction_cannot_be_turned_off()
    {
        var (c, h) = Make(_ => HttpStatusCode.OK, extra: new PassThrough());
        await c.EvaluateAsync("TCKN 10000000146 ve ali@ornek.com", Q, TestContext.Current.CancellationToken);
        Assert.DoesNotContain("10000000146", h.Bodies[0]);
        Assert.DoesNotContain("ali@ornek.com", h.Bodies[0]);
        Assert.Contains("[REDAKTE:tckn]", h.Bodies[0]);
    }
}

public class RedactorTests
{
    public static TheoryData<string, string, string> Samples => new()
    {
        { "anahtar", "sk-" + new string('a', 24), "[REDAKTE:anahtar]" },
        { "iban", "TR33 0006 1005 1978 6457 8413 26", "[REDAKTE:iban]" },
        { "kart", "4111 1111 1111 1111", "[REDAKTE:kart]" },
        { "tckn", "10000000146", "[REDAKTE:tckn]" },
        { "telefon", "0532 123 45 67", "[REDAKTE:telefon]" },
        { "e-posta", "ali@ornek.com", "[REDAKTE:e-posta]" },
    };

    [Theory]
    [MemberData(nameof(Samples))]
    public void Masks_pattern(string kind, string raw, string mask)
    {
        var s = TurkishRedactor.Instance.Redact($"önce {raw} sonra");
        Assert.DoesNotContain(raw, s);
        Assert.Contains(mask, s);
        Assert.NotEmpty(kind);
    }

    [Fact]
    public void Non_luhn_digits_are_not_cards() =>
        Assert.Equal("sipariş 4111 1111 1111 1112", TurkishRedactor.Instance.Redact("sipariş 4111 1111 1111 1112"));
}

public class JevBandsTests
{
    [Theory]
    [InlineData(0.85, Band.Act)]
    [InlineData(0.8499, Band.Flag)]
    [InlineData(0.60, Band.Flag)]
    [InlineData(0.5999, Band.Escalate)]
    public void Band_edges(double k, Band expected) => Assert.Equal(expected, new JevBands().Of(k));

    [Theory]
    [InlineData(0.1, 0.9, Band.Act)]
    [InlineData(0.95, 0.95, Band.Act)]
    [InlineData(0.5, 0.5, Band.Escalate)]
    public void Noul_certainty_is_max_p_1_minus_p(double p, double certainty, Band expected)
    {
        var a = new JevAnswer("noul", p, null, null, null, null);
        Assert.Equal(certainty, JevBands.Certainty(a), 6);
        Assert.Equal(expected, new JevBands().Of(a));
    }

    [Fact]
    public void Options_override_defaults() => Assert.Equal(Band.Escalate, new JevBands(0.95, 0.9).Of(0.89));
}
