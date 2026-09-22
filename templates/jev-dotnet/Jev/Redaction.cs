using System.Text.RegularExpressions;

namespace Jev;

/// <summary>Ek redaksiyon katmanı (alan adları, müşteri no...). TR maskelemenin yerine geçmez.</summary>
public interface IStateRedactor
{
    string Redact(string state);
}

/// <summary>tools/jev/jev/cekirdek.py REDAKSIYON portu: anahtar · IBAN · kart (Luhn) · TCKN · telefon · e-posta.</summary>
public sealed partial class TurkishRedactor : IStateRedactor
{
    public static readonly TurkishRedactor Instance = new();

    static readonly (string Kind, Regex Pattern)[] Patterns =
    [
        ("anahtar", Key()), ("iban", Iban()), ("kart", Card()), ("tckn", Tckn()), ("telefon", Phone()), ("e-posta", Email()),
    ];

    public string Redact(string state)
    {
        foreach (var (kind, pattern) in Patterns)
            state = pattern.Replace(state, m => kind != "kart" || Luhn(m.Value) ? $"[REDAKTE:{kind}]" : m.Value);
        return state;
    }

    static bool Luhn(string s)
    {
        var digits = s.Where(char.IsAsciiDigit).Select(c => c - '0').Reverse().ToArray();
        var sum = digits.Select((d, i) => i % 2 == 1 ? (d * 2 > 9 ? d * 2 - 9 : d * 2) : d).Sum();
        return sum % 10 == 0;
    }

    [GeneratedRegex(@"\bsk-[A-Za-z0-9_-]{20,}|\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_\w{40,}|\bAKIA[0-9A-Z]{16}\b|\bxox[bpas]-[A-Za-z0-9-]{10,}|\bAIza[0-9A-Za-z_-]{35}|(?i:bearer)\s+\S{16,}")]
    private static partial Regex Key();
    [GeneratedRegex(@"\bTR\d{2}(?:\s?\d{4}){5}\s?\d{2}\b", RegexOptions.IgnoreCase)]
    private static partial Regex Iban();
    [GeneratedRegex(@"\b\d(?:[ -]?\d){12,18}\b")]
    private static partial Regex Card();
    [GeneratedRegex(@"\b[1-9]\d{10}\b")]
    private static partial Regex Tckn();
    [GeneratedRegex(@"(?:\+90|\b0)[\s-]?\(?[2-5]\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}\b")]
    private static partial Regex Phone();
    [GeneratedRegex(@"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")]
    private static partial Regex Email();
}
