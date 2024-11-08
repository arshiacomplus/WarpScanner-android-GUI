package org.beeware.android;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Handler;
import android.os.Looper;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class VersionChecker {
    public static void checkVersion(Activity activity) {
        if (!isInternetAvailable(activity)) {
            showNoInternetDialog(activity);
            return;
        }

        new Thread(new Runnable() {
            @Override
            public void run() {
                String link = "https://raw.githubusercontent.com/arshiacomplus/WarpScanner-android-GUI/refs/heads/main/android-toga/version.txt";
                String content = getContentFromURL(link);
                if (!"v0.0.9".equals(content.trim())) {
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

    private static boolean isInternetAvailable(Context context) {
        ConnectivityManager cm = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        return activeNetwork != null && activeNetwork.isConnectedOrConnecting();
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

    private static void showNoInternetDialog(Activity activity) {
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        builder.setMessage("اتصال به اینترنت برقرار نیست. لطفاً اتصال خود را بررسی کنید.")
                .setCancelable(false)
                .setPositiveButton("باشه", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.dismiss();
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();
    }
}
