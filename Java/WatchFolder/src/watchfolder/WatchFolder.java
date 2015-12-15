/**
 * From http://javapapers.com/core-java/monitor-a-folder-using-java/
 * I need to learn it and redoing it for some purpose,
 * not just copas and run without purposes
 * TODO 16 December 2015
*/
package watchfolder;

import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardWatchEventKinds;
import java.nio.file.WatchEvent;
import java.nio.file.WatchKey;
import java.nio.file.WatchService;

public class WatchFolder {
    public static void main(String[] args) throws IOException,
            InterruptedException {
        Path faxFolder = Paths.get("./data/");
        WatchService watchService = FileSystems.getDefault().newWatchService();
        faxFolder.register(watchService, StandardWatchEventKinds.ENTRY_CREATE);

        boolean valid = true;
        do {
                WatchKey watchKey = watchService.take();

                for (WatchEvent event : watchKey.pollEvents()) {
                        WatchEvent.Kind kind = event.kind();
                        if (StandardWatchEventKinds.ENTRY_CREATE.equals(event.kind())) {
                                String fileName = event.context().toString();
                                System.out.println("File Created: " + fileName);
                        }
                }
                valid = watchKey.reset();

        } while (valid);
    }
}
