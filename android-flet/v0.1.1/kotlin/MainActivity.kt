package com.arshiacomplus.warpscanner.warpscanner // << پکیج نیم شما

import android.os.Build // <<<< این import برای چک کردن نسخه اندروید لازم است >>>>
import android.os.Bundle
import android.os.Environment // <<<< این import برای چک کردن نتیجه MANAGE_ALL_FILES لازم است >>>>
import android.util.Log
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
// import java.lang.ref.WeakReference // Alternative approach (less needed here)

class MainActivity: FlutterActivity() {

    companion object {
        private const val TAG = "MainActivityKt"
        @JvmField
        var currentActivityInstance: MainActivity? = null
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        currentActivityInstance = this
        Log.i(TAG, "MainActivity instance created and static reference stored: $this")

        // --- درخواست مجوز مدیریت تمام فایل‌ها (MANAGE_EXTERNAL_STORAGE) ---
        // این کد فقط در اندروید 11 (API 30) و بالاتر اجرا می‌شود.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            // فقط اگر مجوز از قبل داده نشده، کاربر را به تنظیمات بفرست
            if (!Environment.isExternalStorageManager()) {
                 Log.d(TAG, "[Permission Request] Need MANAGE_EXTERNAL_STORAGE. Opening settings...")
                 try {
                     // فراخوانی متد استاتیک از object PermissionUtils
                     // 'this' به عنوان Context و Activity پاس داده می‌شود.
                     // فرض بر این است که PermissionUtils.kt در همین پکیج وجود دارد
                     PermissionUtils.requestManageAllFilesPermission(this, this)
                     // کاربر به تنظیمات هدایت می‌شود. نتیجه مستقیماً برنمی‌گردد.
                 } catch (e: Exception) { // گرفتن Exception کلی برای اطمینان
                     Log.e(TAG, "[Permission Request] Error calling requestManageAllFilesPermission", e)
                 }
            } else {
                 Log.i(TAG, "[Permission Check] MANAGE_EXTERNAL_STORAGE already granted.")
            }
        } else {
             // برای نسخه‌های پایین‌تر، این مجوز لازم نیست یا وجود ندارد.
             Log.i(TAG, "[Permission Check] MANAGE_EXTERNAL_STORAGE not applicable below Android 11.")
        }
        // --------------------------------------------------------------------
    }

    // این متد برای دریافت نتیجه درخواست‌های استاندارد (مثل Storage) است
    // و نتیجه MANAGE_EXTERNAL_STORAGE را دریافت *نمی‌کند*.
    override fun onRequestPermissionsResult(
        requestCode: Int,
        @NonNull permissions: Array<String>,
        @NonNull grantResults: IntArray
    ) {
        Log.d(TAG, "onRequestPermissionsResult received for requestCode: $requestCode")
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        // ارسال نتیجه به PermissionHelper (برای درخواست‌هایی که از پایتون می‌آیند)
        try {
            PermissionHelper.handleRequestPermissionsResult(requestCode, permissions, grantResults)
            Log.d(TAG, "Passed permission result to PermissionHelper.")
        } catch (e: ClassNotFoundException) {
             Log.e(TAG, "FATAL: PermissionHelper class not found!", e)
        } catch (e: NoSuchMethodError) {
             Log.e(TAG, "FATAL: handleRequestPermissionsResult method not found or mismatch!", e)
        } catch (t: Throwable) {
             Log.e(TAG, "Unexpected error calling PermissionHelper.handleRequestPermissionsResult", t)
        }
    }

    // **مهم:** برای چک کردن نتیجه MANAGE_EXTERNAL_STORAGE
    // باید از onResume استفاده کنید.
    override fun onResume() {
        super.onResume()
        Log.d(TAG, "onResume called.")
        // چک کردن وضعیت مجوز مدیریت فایل‌ها وقتی کاربر به برنامه برمی‌گردد
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            val hasManagePermission = Environment.isExternalStorageManager()
            Log.i(TAG, "[Permission Check onResume] MANAGE_EXTERNAL_STORAGE Granted: $hasManagePermission")
            // اینجا می‌توانید بر اساس وضعیت مجوز، کاری انجام دهید
            // مثلاً یک پیام به کاربر نشان دهید یا قابلیتی را فعال/غیرفعال کنید.
            // توجه: ارسال مستقیم نتیجه به پایتون از اینجا کمی پیچیده‌تر است.
        }
    }


    override fun onDestroy() {
        super.onDestroy()
        Log.i(TAG, "MainActivity instance being destroyed: $this")
        if (currentActivityInstance == this) {
             currentActivityInstance = null
             Log.i(TAG, "Static MainActivity instance reference cleared.")
        } else {
             Log.w(TAG, "onDestroy called, but static instance was already different or null.")
        }
    }
}