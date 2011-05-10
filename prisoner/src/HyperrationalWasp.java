import java.util.*;

public class HyperrationalWasp
{
    // I'm avoiding enums so as not to clutter up the warriors directory with extra class files.
    private static String Clam = "c";
    private static String Rat = "t";
    private static String Ambiguous = "x";

    private static final String PROLOGUE = "ttc";

    private static int n;
    private static String myActions;
    private static String hisActions;

    private static String decideMove() {
        if (n < PROLOGUE.length()) return PROLOGUE.substring(n, n+1);

        // KISS - rather an easy special case here than a complex one later
        if (mirrorMatch()) return Clam;
        if (n == 99) return Rat; // This is rational rather than superrational

        int memory = estimateMemory();
        if (memory == 0) return Rat; // I don't think the opponent will punish me
        if (memory > 0) {
            Map<String, String> memoryModel = buildMemoryModel(memory);
            String myRecentHistory = myActions.substring(0, memory - 1);
            // I don't think the opponent will punish me.
            if (Clam.equals(memoryModel.get(Rat + myRecentHistory))) return Rat;
            // I think the opponent will defect whatever I do.
            if (Rat.equals(memoryModel.get(Clam + myRecentHistory))) return Rat;
            // Opponent will cooperate unless I defect.
            return Clam;
        }

        // Haven't figured out opponent's strategy. Tit for tat is a reasonable fallback.
        return hisAction(0);
    }

    private static int estimateMemory() {
        if (hisActions.substring(0, n-1).equals(hisActions.substring(1, n))) return 0;

        int memory = -1; // Superrational?
        for (int probe = 1; probe < 5; probe++) {
            Map<String, String> memoryModel = buildMemoryModel(probe);
            if (memoryModel.size() <= 1 || memoryModel.values().contains(Ambiguous)) {
                break;
            }
            memory = probe;
        }

        if (memory == -1 && isOpponentRandom()) return 0;

        return memory;
    }

    private static boolean isOpponentRandom() {
        // We only call this if the opponent appears not have have a small fixed memory,
        // so there's no point trying anything complicated. This is supposed to be a Wilson
        // confidence test, although my stats is so rusty there's a 50/50 chance that I've
        // got the two probabilities (null hypothesis of 0.5 and observed) the wrong way round.
        if (n < 10) return false; // Not enough data.
        double p = count(hisActions, Clam) / (double)n;
        double z = 2;
        double d = 1 + z*z/n;
        double e = p + z*z/(2*n);
        double var = z * Math.sqrt(p*(1-p)/n + z*z/(4*n*n));
        return (e - var) <= 0.5 * d && 0.5 * d <= (e + var);
    }

    private static Map<String, String> buildMemoryModel(int memory) {
        // It's reasonable to have a hard-coded prologue to probe opponent's behaviour,
        // and that shouldn't be taken into account.
        int skip = 0;
        if (n > 10) skip = n / 2;
        if (skip > 12) skip = 12;

        Map<String, String> memoryModel = buildMemoryModel(memory, skip);
        // If we're not getting any useful information after skipping prologue, take it into account.
        if (memoryModel.size() <= 1 && !memoryModel.values().contains(Ambiguous)) {
            memoryModel = buildMemoryModel(memory, 0);
        }
        return memoryModel;
    }

    private static Map<String, String> buildMemoryModel(int memory, int skip) {
        Map<String, String> model = new HashMap<String, String>();
        for (int off = 0; off < n - memory - 1 - skip; off++) {
            String result = hisAction(off);
            String hypotheticalCause = myActions.substring(off+1, off+1+memory);
            String prev = model.put(hypotheticalCause, result);
            if (prev != null && !prev.equals(result)) model.put(hypotheticalCause, Ambiguous);
        }
        return model;
    }

    private static boolean mirrorMatch() { return hisActions.matches("c*ctt"); }
    private static String myAction(int idx) { return myActions.substring(idx, idx+1).intern(); }
    private static String hisAction(int idx) { return hisActions.substring(idx, idx+1).intern(); }
    private static int count(String actions, String action) {
        int count = 0;
        for (int idx = 0; idx < actions.length(); ) {
            int off = actions.indexOf(action, idx);
            if (off < 0) break;
            count++;
            idx = off + 1;
        }
        return count;
    }

    public static void main(String[] args) {
        if (args.length == 0) {
            hisActions = myActions = "";
            n = 0;
        }
        else {
            n = args[0].length();
            myActions = args[0].replaceAll("[KR]", Clam).replaceAll("[SE]", Rat);
            hisActions = args[0].replaceAll("[KS]", Clam).replaceAll("[RE]", Rat);
        }

        System.out.println(decideMove());
    }

}
