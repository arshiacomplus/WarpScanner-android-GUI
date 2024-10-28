package org.beeware.android;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Handler;
import android.os.Looper;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class VersionChecker {

    public static void checkVersion(Activity activity) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                String link = "https://raw.githubusercontent.com/arshiacomplus/WarpScanner-android-GUI/refs/heads/main/android-toga/version.txt";
                String content = getContentFromURL(link);

                if (!"v0.0.4".equals(content.trim())) {
                    // نمایش دیالوگ در نخ اصلی
                    new Handler(Looper.getMainLooper()).post(new Runnable() {
                        @Override
                        public void run() {
                            showUpdateDialog(activity);
                        }
                    });
                }
            }
        }).start();
    }

    private static String getContentFromURL(String link) {
        StringBuilder content = new StringBuilder();
        try {
            URL url = new URL(link);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;

            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return content.toString();
    }

    private static void showUpdateDialog(Activity activity) {
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        builder.setMessage("بروزرسانی در دسترس است")
                .setCancelable(false)
                .setPositiveButton("برو", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://github.com/arshiacomplus/WarpScanner-android-GUI/"));
                        activity.startActivity(browserIntent);
                    }
                })
                .setNegativeButton("بستن", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.dismiss();
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();
    }
}
