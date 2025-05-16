package com.arshiacomplus.warpscanner.warpscanner // << پکیج نیم شما

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.util.Log
import androidx.annotation.NonNull
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterActivity

class MainActivity: FlutterActivity() {

    companion object {
        private const val TAG = "MainActivityKt"
        // کد درخواست یکسان برای مجوزهای قدیمی در همه نسخه‌ها
        private const val LEGACY_STORAGE_REQUEST_CODE = 101
        @JvmField
        var currentActivityInstance: MainActivity? = null
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        currentActivityInstance = this
        Log.i(TAG, "onCreate: MainActivity instance created: $this")
        Log.i(TAG, "onCreate: Android SDK Version: ${Build.VERSION.SDK_INT}")

        checkAndRequestPermissions()
    }

    private fun checkAndRequestPermissions() {
        Log.d(TAG, "checkAndRequestPermissions: Starting permission check...")
        // --- بررسی و درخواست مجوز بر اساس نسخه اندروید ---
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            // --- Android 11 (API 30) and higher ---
            Log.i(TAG, "checkAndRequestPermissions: Running on Android 11+.")
            try {
                 val isManageStorageGranted = Environment.isExternalStorageManager()
                 Log.d(TAG,"checkAndRequestPermissions: MANAGE_EXTERNAL_STORAGE granted? $isManageStorageGranted")

                if (!isManageStorageGranted) {
                     Log.w(TAG, "[Permission Request] MANAGE_EXTERNAL_STORAGE not granted.")
                     // 1. کاربر را به تنظیمات برای مجوز مدیریت فایل بفرست
                     Log.i(TAG,"[Permission Request] Attempting to open settings for MANAGE_EXTERNAL_STORAGE via PermissionUtils...")
                     try {
                         PermissionUtils.requestManageAllFilesPermission(this, this)
                         Log.i(TAG, "[Permission Request] Call to PermissionUtils.requestManageAllFilesPermission completed.")
                     } catch (e: Exception) {
                         Log.e(TAG, "[Permission Request] CRITICAL: Error calling PermissionUtils.requestManageAllFilesPermission", e)
                     }

                     // 2. (طبق درخواست جدید) همچنین مجوزهای قدیمی را هم درخواست بده (داخل try-catch)
                     Log.i(TAG, "[Permission Request] Also checking and requesting legacy permissions on Android 11+ (as requested)...")
                     checkAndRequestLegacyPermissions(" (on Android 11+)") // یک پسوند برای لاگ اضافه میکنیم

                } else {
                     Log.i(TAG, "[Permission Check] MANAGE_EXTERNAL_STORAGE already granted. No further requests needed.")
                     // وقتی مجوز کامل داریم، نیازی به درخواست قدیمی‌ها نیست.
                }
            } catch (e: Exception) {
                 Log.e(TAG, "checkAndRequestPermissions: CRITICAL: Error checking or requesting MANAGE_EXTERNAL_STORAGE", e)
            }

        } else {
             // --- Android 10 (API 29) and lower ---
             Log.i(TAG, "checkAndRequestPermissions: Running on Android < 11.")
             // فقط مجوزهای قدیمی را چک و درخواست کن
             checkAndRequestLegacyPermissions(" (on Android < 11)")
        }
        Log.d(TAG, "checkAndRequestPermissions: Finished permission check logic.")
    }

    /**
     * متد کمکی برای چک و درخواست مجوزهای قدیمی READ/WRITE_EXTERNAL_STORAGE
     * @param logSuffix پسوندی برای اضافه کردن به لاگ‌ها جهت تشخیص سناریو
     */
    private fun checkAndRequestLegacyPermissions(logSuffix: String = "") {
        val hasReadPermission = ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED
        // WRITE_EXTERNAL_STORAGE در اندروید 11+ رفتار متفاوتی دارد و ممکن است همیشه قابل دریافت نباشد
        val hasWritePermission = ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED
        Log.d(TAG, "checkAndRequestLegacyPermissions$logSuffix: READ granted: $hasReadPermission, WRITE granted: $hasWritePermission")

        val permissionsToRequest = mutableListOf<String>()
        if (!hasReadPermission) permissionsToRequest.add(Manifest.permission.READ_EXTERNAL_STORAGE)
        if (!hasWritePermission) permissionsToRequest.add(Manifest.permission.WRITE_EXTERNAL_STORAGE)

        if (permissionsToRequest.isNotEmpty()) {
            Log.i(TAG, "[Permission Request] Need legacy permissions$logSuffix: ${permissionsToRequest.joinToString()}. Requesting...")
            // --- بلوک Try-Catch طبق درخواست ---
            try {
                ActivityCompat.requestPermissions(
                    this,
                    permissionsToRequest.toTypedArray(), // فقط مجوزهای لازم را درخواست بده
                    LEGACY_STORAGE_REQUEST_CODE // کد برای شناسایی نتیجه
                )
                Log.i(TAG, "[Permission Request] ActivityCompat.requestPermissions for legacy permissions called$logSuffix.")
            } catch (e: Exception) {
                // گرفتن Exception کلی برای اطمینان
                Log.e(TAG, "[Permission Request] CRITICAL: Error calling ActivityCompat.requestPermissions for legacy$logSuffix", e)
            }
            // ------------------------------------
        } else {
            Log.i(TAG, "[Permission Check] Legacy storage permissions already granted$logSuffix.")
        }
    }

    // این متد برای دریافت نتیجه درخواست‌های *استاندارد* (مثل READ/WRITE) است
    override fun onRequestPermissionsResult(
        requestCode: Int,
        @NonNull permissions: Array<String>,
        @NonNull grantResults: IntArray
    ) {
        Log.i(TAG, "onRequestPermissionsResult: Received result for requestCode: $requestCode")
        super.onRequestPermissionsResult(requestCode, permissions, grantResults) // فراخوانی والد مهمه

        // پردازش نتیجه برای کد درخواست مجوزهای قدیمی
        if (requestCode == LEGACY_STORAGE_REQUEST_CODE) {
            val grantedMap = permissions.zip(grantResults.toTypedArray()).toMap()
            Log.i(TAG, "onRequestPermissionsResult: Result for LEGACY_STORAGE_REQUEST_CODE. Results: $grantedMap")
            // می‌توانید نتایج دقیق‌تر را لاگ کنید
             grantedMap.forEach { (permission, grantResult) ->
                 Log.d(TAG, "  Permission: $permission, Granted: ${grantResult == PackageManager.PERMISSION_GRANTED}")
             }
        }

        // ارسال نتیجه به PermissionHelper (همیشه انجام شود)
        try {
            PermissionHelper.handleRequestPermissionsResult(requestCode, permissions, grantResults)
            Log.d(TAG, "onRequestPermissionsResult: Passed permission result to PermissionHelper.")
        } catch (e: Throwable) {
             Log.e(TAG, "onRequestPermissionsResult: CRITICAL: Error calling PermissionHelper.handleRequestPermissionsResult", e)
        }
    }

    // چک کردن نتیجه MANAGE_EXTERNAL_STORAGE در onResume (بدون تغییر)
    override fun onResume() {
        super.onResume()
        Log.i(TAG, "onResume: Activity resumed.")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            try {
                val hasManagePermission = Environment.isExternalStorageManager()
                Log.i(TAG, "onResume: [Permission Check] MANAGE_EXTERNAL_STORAGE Granted after returning: $hasManagePermission")
            } catch (e: Exception) {
                 Log.e(TAG, "onResume: CRITICAL: Error checking MANAGE_EXTERNAL_STORAGE in onResume", e)
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.i(TAG, "onDestroy: MainActivity instance being destroyed: $this")
        if (currentActivityInstance == this) {
             currentActivityInstance = null
             Log.i(TAG, "onDestroy: Static MainActivity instance reference cleared.")
        }
    }
}