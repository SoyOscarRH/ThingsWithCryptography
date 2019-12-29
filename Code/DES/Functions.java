
import java.math.BigInteger;
import java.util.Deque;
import java.util.LinkedList;

public class Functions {

    static public String ConverToFinal(String Binary) {

        long decimal = Long.parseLong(Binary, 2);
        String Hexa = "";

        return Long.toHexString(decimal);
    }

    static public String ConvertoToBin(String Key) {

        System.out.println("Llave: " + Key);

        char cadChar[] = Key.toCharArray();

        int longitud = Key.length();
        int Dec[] = new int[longitud];
        String Hexa = "";
        String Bin = "";
        String Final = "";
        int Completar;

        for (int i = 0; i < longitud; i++) {

            Dec[i] = (int) cadChar[i];

            Hexa += Integer.toHexString(Dec[i]);

        }

        Bin = new BigInteger(Hexa, 16).toString(2);

        if (Bin.length() < 64) {

            Completar = 64 - Bin.length();

            for (int i = 0; i < Completar; i++) {

                Final += "0";

            }

            Final += Bin;

        }

        System.out.println("Key en binario = " + Final);
        System.out.println("Bits Key = " + Final.length());

        return Final;

    }

    static public String PC_1(String Binary) {

        char cadChar[] = Binary.toCharArray();
        String BinaryPC = "";

        int PC[] = { 57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52,
                44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28,
                20, 12, 4 };
        int aux;

        for (int i = 0; i < 56; i++) {

            aux = PC[i];
            aux = aux - 1;
            BinaryPC += cadChar[aux];
            

        }

        System.out.println("PC-1(Key) = " + BinaryPC);
        System.out.println("Bits PC-1(Key) = " + BinaryPC.length());
        System.out.println("PC-1(Key) Hexa = " + ConverToFinal(BinaryPC));

        return BinaryPC;

    }

    static public String Shift(String Binary, int S) {

        char cadChar[] = Binary.toCharArray();
        int Round[] = { 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1 };

        Deque<String> Co = new LinkedList();
        Deque<String> Do = new LinkedList();

        for (int i = 0; i < 28; i++) {

            Co.add("" + cadChar[i]);

        }

        System.out.println("Co = " + Co);

        for (int i = 28; i < 56; i++) {

            Do.add("" + cadChar[i]);

        }

        System.out.println("Do = " + Do);

        int Shift = 0;

        System.out.println("Round = " + S);

        for (int k = 0; k < S; k++) {

            Shift += Round[k];

        }

        System.out.println("Shift = " + Shift);
        String aux, aux2;

        for (int j = 0; j < Shift; j++) {

            aux = Co.getLast();
            Co.removeLast();
            Co.addFirst(aux);

            aux2 = Do.getLast();
            Do.removeLast();
            Do.addFirst(aux2);

        }

        System.out.println("Co = " + Co);
        System.out.println("Do = " + Do);

        String ShiftBinary = "";

        for (int i = 0; i < 28; i++) {

            ShiftBinary += Co.getFirst();
            Co.removeFirst();

        }

        for (int i = 0; i < 28; i++) {

            ShiftBinary += Do.getFirst();
            Do.removeFirst();

        }

        System.out.println("Co+Do = " + ShiftBinary);
        System.out.println("Bits of Co+Do = " + ShiftBinary.length());

        return ShiftBinary;

    }

    static public String PC_2(String Binary) {

        char cadChar[] = Binary.toCharArray();
        String BinaryPC = "";

        int PC[] = { 14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31,
                37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32 };
        int aux;

        for (int i = 0; i < 48; i++) {

            aux = PC[i];
            aux = aux - 1;
            BinaryPC += cadChar[aux];

        }

        System.out.println("PC-2(Co+Do)= " + BinaryPC);
        System.out.println("Bits of PC-2(Co+Do) = " + BinaryPC.length());

        return BinaryPC;

    }

    public static void main(String[] args) {
        var key = ConvertoToBin("Asegurar");

        var pc1 = PC_1(key);
    }
}