namespace Jev;

// JSON: System.Text.Json web varsayılanları (camelCase) → type · instructions · criteria · noul · choice · probabilities.
public sealed record JevQuestion(string Type, string Instructions, object? Criteria = null);

public sealed record JevAnswer(string Type, double? Noul, string? Choice, double? Score,
    Dictionary<string, double>? Probabilities, double? Confidence);

public sealed record JevRequest(string Model, string State, IReadOnlyDictionary<string, JevQuestion> Questions);

public sealed record JevResponse(Dictionary<string, JevAnswer> Answers);

public sealed class JevOptions
{
    public string BaseUrl { get; set; } = "https://openrouter.ai/api/v1/";   // TypeSafe: https://api.typesafe.ai/v1/
    public string ApiKey { get; set; } = "";                                 // ortamdan/secret store'dan; loglanmaz
    public string Model { get; set; } = "jev-1.13";
    public int MaxBatches { get; set; } = 5;       // batch tavanı: ≤ChunkSize state'lik parça sayısı
    public int MaxRequests { get; set; } = 250;    // HTTP tavanı: tekrarlar dahil
    public int Retries { get; set; } = 2;
    public int ChunkSize { get; set; } = 200;
    public int MaxConcurrency { get; set; } = 8;
    public double Act { get; set; } = 0.85;
    public double Flag { get; set; } = 0.60;
}

public sealed class JevLimitException(string message) : Exception(message);
