import java.lang.Exception;
import java.util.Arrays;

/**
 * @author Garcia De Santiago Jorge Luis
 * @author Rosas Hernandez Oscar Andres
 */
class MatrixUtils {
    /**
     * Gets the determinant of a matrix (it is given that the matrix is square)
     */
    private static int determinant(final int[][] matrix) {
        final var n = matrix.length;

        if (n == 1)
            return matrix[0][0];
        else if (n == 2)
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];

        var determinant = 0;

        for (int i = 0; i < n; i++) {
            var temporal = new int[n - 1][n - 1];

            for (int j = 0; j < n; j++) {
                if (j == i)
                    continue;

                for (int k = 1; k < n; k++) {
                    int index = j < i ? j : j - 1;
                    temporal[index][k - 1] = matrix[j][k];
                }
            }

            var temporalValue = matrix[i][0] * determinant(temporal);
            determinant += i % 2 == 0 ? temporalValue : -temporalValue;
        }

        return determinant;
    }

    /**
     * Multiply a matrix by a value (this edit the value)
     */
    public static void multiplyValue(int[][] matrix, int n, int mod) {
        final var size = matrix.length;

        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                matrix[i][j] = backToMod(n * matrix[i][j], mod);
            }
        }
    }

    public static int[][] cofactorMatrix(final int[][] matrix, int mod) {
        var cofactors = new int[matrix.length][matrix.length];

        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix.length; j++) {

                var matrixDeterminant = new int[matrix.length - 1][matrix.length - 1];

                for (int k = 0; k < matrix.length; k++) {
                    if (k != i) {
                        for (int l = 0; l < matrix.length; l++) {

                            if (l != j) {
                                var x = k < i ? k : k - 1;
                                var y = l < j ? l : l - 1;
                                matrixDeterminant[x][y] = backToMod(matrix[k][l], mod);
                            }
                        }
                    }
                }

                final var detValor = determinant(matrixDeterminant);
                cofactors[i][j] = backToMod(detValor * (int) Math.pow(-1, i + j + 2), mod);
            }
        }
        return cofactors;
    }

    public static int[][] matrixTranspuesta(int[][] matrix, int mod) {
        var transposeMatrix = new int[matrix[0].length][matrix.length];

        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix.length; j++) {
                transposeMatrix[i][j] = backToMod(matrix[j][i], mod);
            }
        }
        return transposeMatrix;
    }

    private static int greatestCommonDivisor(int n, int m) {
        var a = Math.max(n, m);
        var b = Math.min(n, m);
        var result = 0;

        do {
            result = b;
            b = a % b;
            a = result;
        } while (b != 0);

        return result;
    }

    public static boolean isInvertibleModN(final int[][] matrix, int n) {
        return greatestCommonDivisor(determinant(matrix), n) == 1;
    }

    public static void print2D(int matrix[][]) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static int backToMod(int a, int mod) {
        if (a < 0) {
            a = Math.abs(a) % mod;
            a = mod - a;
        } else {
            a = a % mod;
        }

        return a;
    }

    private static int modularInverse(int a, int m) {
        a = backToMod(a, m);
        int r0 = a, r1 = m, ri, s0 = 1, s1 = 0, si;

        while (r1 != 0) {
            si = s0 - s1 * (r0 / r1);
            s0 = s1;
            s1 = si;
            ri = r0 % r1;
            r0 = r1;
            r1 = ri;
        }
        if (r0 < 0)
            s0 *= -1;
        if (s0 < 0)
            s0 += m;
        return s0;
    }

    public static int[][] inverseMatrixModN(int[][] matrix, int mod) {
        final var determinantInv = modularInverse(determinant(matrix), mod);
        var cofactorMatrix = matrixTranspuesta(cofactorMatrix(matrix, mod), mod);
        multiplyValue(cofactorMatrix, determinantInv, mod);

        return cofactorMatrix;
    }
}

/**
 * Code and decode messages
 *
 * @author Garcia De Santiago Jorge Luis
 * @author Rosas Hernandez Oscar Andres
 */
public class Hill {

    /*
     * A B C D E F G H I J K  L  M  N  Ñ  O  P  Q  R  S  T  U  V  W  X  Y  Z 
     * 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
     */
    final static String alphabetMayus = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ";

    /**
     * Gets the matrix key, the values of the matrix represent the position of the
     * letter in the alphabet.
     *
     * @param key The text from where we will create the matrix
     * @return matrix key
     */
    private static int[][] getMatrixKey(final String key) throws Exception {
        var matrixDimensions = Math.sqrt(key.length());
        if ((matrixDimensions - Math.floor(matrixDimensions)) != 0)
            throw new Exception("Llave inválida, no se puede formar una matrix n x n con dicha key");

        var n = (int) matrixDimensions;
        var matrixKey = new int[n][n];
        var currentIndex = 0;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                var numericValue = alphabetMayus.indexOf(key.charAt(currentIndex));
                if (numericValue == -1)
                    throw new Exception("Llave inválida, esta tiene caracteres no presentes en el alfabeto");

                matrixKey[i][j] = numericValue;
                currentIndex++;
            }
        }

        // Matrix key should be invertible mod 27
        if (!MatrixUtils.isInvertibleModN(matrixKey, n))
            throw new Exception("La matrix generada no es invertible, no es una key válida");

        return matrixKey;
    }

    /**
     * Cifra un texto con Cifrado de Hill, simplemente multiplica, no tiene mucha magia
     *
     * @param message The text to encode
     * @param Key     The matrix to encoded (it is supose valid)
     * @return encodedMessage The cipher text
     */
    private static String encode(final String message, final int[][] key) throws Exception {
        var encodedMessage = "";
        var messageLeftToEncode = new String(message);

        var block = "";
        final var blockSize = key.length;
        final var modN = alphabetMayus.length();

        int[][] matrixValues = new int[1][key.length];
        int[][] encodedMatrix = new int[1][key.length];

        if (message.length() % blockSize != 0) {
            var fillValue = 'A';
            var times = 3 - (message.length() % blockSize);
            var padding = new char[times];
            Arrays.fill(padding, fillValue);

            messageLeftToEncode += new String(padding);
        }

        while (messageLeftToEncode.length() > 0) {
            block = messageLeftToEncode.substring(0, blockSize);

            for (int i = 0; i < blockSize; i++) {
                var index = alphabetMayus.indexOf(block.charAt(i));
                if (index == -1)
                    throw new Exception("El mensaje contiene caracteres que no estan en el alfabeto");

                matrixValues[0][i] = index;
            }

            // Encode (the good part matrix multiplication)
            for (int i = 0; i < blockSize; i++) {
                var value = 0;

                for (int j = 0; j < matrixValues[0].length; j++)
                    value += key[i][j] * matrixValues[0][j];

                encodedMatrix[0][i] = value % modN;
            }

            // From matrix to text
            for (int i = 0; i < blockSize; i++)
                encodedMessage += alphabetMayus.charAt(encodedMatrix[0][i]);

            messageLeftToEncode = messageLeftToEncode.substring(blockSize);
        }

        encodedMessage = encodedMessage.substring(0, message.length());

        return encodedMessage;
    }

    /**
     * Elimina caracteres que no estan en el alfabeto
     *
     * @param message The text to encode
     */
    private static String filterOtherCharacters(final String message) {
        var filtered = "";
        for (int i = 0; i < message.length(); i++) {
            var index = alphabetMayus.indexOf(message.charAt(i));
            if (index != -1) {
                filtered += alphabetMayus.charAt(index);
            }
        }

        return filtered;
    }

    /**
     * Inserta los caracteres especiales que estan en original que no estan en el string message
     */
    private static String addOtherCharacters(final String message, final String original) {
        var result = "";
        var messageIndex = 0;

        for (int i = 0; i < original.length(); i++) {
            var index = alphabetMayus.indexOf(original.charAt(i));
            if (index == -1)
                result += original.charAt(i);
            else
                result += message.charAt(messageIndex++);
        }

        return result;
    }

    /**
     * Lo bonito de Hill es que es asi de sencillo decodificar
     */
    private static String decode(final String message, final int[][] decodeKey) throws Exception {
        return encode(message, decodeKey);
    }

    public static void main(String[] args) {
        try {
            // String message = "CUADERNODECULTURACIENTIFICA";
            String message = "DIVULGANDO LAS MATEMATICAS :) HOLA BEBE";

            String key = "FORTALEZA";
            // String key = "BCDAEFBAG";

            // 1. Texto original
            System.out.println("Texto original:   " + message);
            System.out.println("Llave:            " + key);
            System.out.println();

            // 2. Codificar
            var matrixKey = getMatrixKey(key);
            System.out.println("Matriz llave:");
            MatrixUtils.print2D(matrixKey);

            String encodedMessage = encode(filterOtherCharacters(message), matrixKey);
            encodedMessage = addOtherCharacters(encodedMessage, message);
            System.out.println("Texto codificado: " + encodedMessage);
            System.out.println();



            // FROM NOW ON WE ONLY KNOW THE KEY AND THE ENCODED MESSAGE


            // 3. Decodificar
            var matrixInverseKey = MatrixUtils.inverseMatrixModN(matrixKey, Hill.alphabetMayus.length());
            System.out.println("Matriz de decodificacion:");
            MatrixUtils.print2D(matrixInverseKey);

            String decodedMessage = decode(filterOtherCharacters(encodedMessage), matrixInverseKey);
            decodedMessage = addOtherCharacters(decodedMessage, encodedMessage);

            System.out.println("Texto decodificado: " + decodedMessage);

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}