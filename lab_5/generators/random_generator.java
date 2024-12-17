import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class random_generator {
    /**
     * Generate a random bit sequence and save it to a file.
     * @param filename: The path to the file where the random sequence will be saved.
     */
    public static void main(String[] args) {
        String filename = "C:\\Users\\79297\\Desktop\\isb\\lab_2\\random_sequence_java.txt";
        try {
            File file = new File(filename);
            File directory = file.getParentFile();
            if (directory != null && !directory.exists()) {
                directory.mkdirs();
            }
            Random random = new Random();
            BufferedWriter writer = new BufferedWriter(new FileWriter(file));
            for (int i = 0; i < 128; ++i) {
                int bit = random.nextInt(2); 
                writer.write(Integer.toString(bit));
            }
            writer.close();
        } catch (IOException e) {
            System.err.println("The file could not be opened for writing");
            e.printStackTrace();
        }
    }
}
