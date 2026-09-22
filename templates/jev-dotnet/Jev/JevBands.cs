namespace Jev;

public enum Band { Act, Flag, Escalate }

/// <summary>Güven bantları. noul için kesinlik max(p, 1−p): 0.1 "kesin hayır" demektir.</summary>
public sealed class JevBands(double act = 0.85, double flag = 0.60)
{
    public static JevBands From(JevOptions o) => new(o.Act, o.Flag);

    public static double Certainty(JevAnswer a) =>
        a.Type == "noul" ? Math.Max(a.Noul ?? 0, 1 - (a.Noul ?? 0)) : a.Confidence ?? 0;

    public Band Of(double certainty) => certainty >= act ? Band.Act : certainty >= flag ? Band.Flag : Band.Escalate;

    public Band Of(JevAnswer a) => Of(Certainty(a));
}
