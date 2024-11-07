package org.beeware.android;

import android.content.Context;
import android.os.Environment;
import java.io.File;
import java.io.IOException;
import java.util.logging.FileHandler;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

public class LoggingConfig {

    public static void setup(Context context) {
        String logPath = Environment.getExternalStorageDirectory().getAbsolutePath() + "/Download/wwarpscanner/app_java.txt";
        File logFile = new File(logPath);

        if (logFile.exists()) {
            logFile.delete();
        }

        try {
            if (logFile.createNewFile()) {
                Handler fileHandler = new FileHandler(logPath, true);
                fileHandler.setFormatter(new SimpleFormatter());
                Logger logger = Logger.getLogger(context.getPackageName());
                logger.addHandler(fileHandler);
                logger.setLevel(Level.ALL);
                Logger.getLogger("").addHandler(fileHandler); // Add handler to root logger
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
