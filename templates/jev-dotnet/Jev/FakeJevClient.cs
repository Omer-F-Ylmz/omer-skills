namespace Jev;

/// <summary>Test ikizi: ağ yok. Yanıtı `respond` üretir; gelen state'ler (redakte edilmiş) `States`'te.</summary>
public sealed class FakeJevClient(Func<string, IReadOnlyDictionary<string, JevQuestion>, IReadOnlyDictionary<string, JevAnswer>> respond) : IJevClient
{
    public List<string> States { get; } = [];

    public Task<IReadOnlyDictionary<string, JevAnswer>> EvaluateAsync(string state, IReadOnlyDictionary<string, JevQuestion> questions, CancellationToken ct = default)
    {
        state = TurkishRedactor.Instance.Redact(state);
        lock (States) States.Add(state);
        return Task.FromResult(respond(state, questions));
    }

    public async Task<IReadOnlyList<IReadOnlyDictionary<string, JevAnswer>>> BatchAsync(IReadOnlyList<string> states, IReadOnlyDictionary<string, JevQuestion> questions, CancellationToken ct = default) =>
        await Task.WhenAll(states.Select(s => EvaluateAsync(s, questions, ct)));
}
