package com.arshiacomplus.warpscanner.warpscanner // << پکیج نیم خودت رو اینجا بذار

import android.Manifest
import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri // لازم برای Intent جدیدتر در MANAGE_ALL_FILES
import android.os.Build
import android.os.Environment
import android.provider.Settings
import android.util.Log // برای لاگ‌گیری خطا
import androidx.annotation.RequiresApi // برای نشان دادن نیاز به نسخه API
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

/**
 * کلاس کمکی برای مدیریت درخواست‌های مجوز در اندروید.
 * از object به جای class استفاده شده چون فقط شامل متدهای استاتیک-مانند است.
 */
object PermissionUtils {

    private const val TAG = "PermissionUtilsKt" // تگ برای لاگ
    private const val STORAGE_PERMISSION_REQUEST_CODE = 101 // کد دلخواه برای درخواست Storage

    /**
     * مجوزهای استاندارد خواندن و نوشتن حافظه خارجی را درخواست می‌کند.
     * (READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE)
     * این متد برای اندروید 10 به پایین حیاتی است و در نسخه‌های بالاتر هم ممکن است لازم باشد.
     *
     * @param activity اکتیویتی فعلی که درخواست از آن ارسال می‌شود.
     */
    @JvmStatic // این انوتیشن اجازه می‌دهد متد مانند یک متد استاتیک جاوا فراخوانی شود
    fun requestStoragePermissions(activity: Activity) {
        // بررسی اینکه آیا مجوزها قبلاً داده شده‌اند یا نه
        val readPermissionGranted = ContextCompat.checkSelfPermission(
            activity, Manifest.permission.READ_EXTERNAL_STORAGE
        ) == PackageManager.PERMISSION_GRANTED

        val writePermissionGranted = ContextCompat.checkSelfPermission(
            activity, Manifest.permission.WRITE_EXTERNAL_STORAGE
        ) == PackageManager.PERMISSION_GRANTED

        // اگر هر کدام از مجوزها داده نشده باشند
        if (!readPermissionGranted || !writePermissionGranted) {
            Log.d(TAG, "Requesting standard storage permissions (READ/WRITE)...")
            // لیست مجوزهایی که باید درخواست شوند
            val permissionsToRequest = arrayOf(
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE
            )
            // نمایش دیالوگ سیستمی درخواست مجوز
            ActivityCompat.requestPermissions(
                activity,
                permissionsToRequest,
                STORAGE_PERMISSION_REQUEST_CODE // کد برای شناسایی نتیجه در onRequestPermissionsResult
            )
        } else {
            Log.d(TAG, "Standard storage permissions (READ/WRITE) already granted.")
            // اگر مجوزها از قبل داده شده‌اند، کاری انجام نمی‌دهیم
            // (می‌توان یک callback برای اطلاع‌رسانی داشت)
        }
    }

    /**
     * درخواست مجوز MANAGE_EXTERNAL_STORAGE برای اندروید 11 (API 30) و بالاتر.
     * این مجوز دسترسی کامل به حافظه خارجی می‌دهد اما نیاز به بررسی دقیق در گوگل پلی دارد.
     * این متد کاربر را به صفحه تنظیمات سیستم هدایت می‌کند.
     *
     * @param context کانتکست برنامه (می‌تواند Activity یا Application Context باشد).
     * @param activity (اختیاری) اگر می‌خواهید از startActivityForResult استفاده کنید (در اینجا لازم نیست).
     */
    @JvmStatic
    @RequiresApi(Build.VERSION_CODES.R) // این متد فقط برای اندروید 11 و بالاتر معنی دارد
    fun requestManageAllFilesPermission(context: Context, activity: Activity? = null) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            // بررسی اینکه آیا برنامه در حال حاضر مجوز MANAGE_EXTERNAL_STORAGE را دارد؟
            if (!Environment.isExternalStorageManager()) {
                Log.d(TAG, "Requesting MANAGE_EXTERNAL_STORAGE permission by opening settings...")
                try {
                    // ایجاد Intent برای باز کردن صفحه تنظیمات مدیریت فایل‌ها
                    val intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                    // اضافه کردن پکیج نیم برنامه به URI تا مستقیماً به تنظیمات همین برنامه برود
                    intent.data = Uri.parse("package:${context.packageName}")

                    // اگر activity داریم، از آن برای شروع استفاده می‌کنیم (بهتر است)
                    if (activity != null) {
                         activity.startActivity(intent) // می‌توان از startActivityForResult هم استفاده کرد اگر نیاز به نتیجه فوری باشد
                    } else {
                        // اگر فقط context داریم (مثلاً از سرویس)، فلگ NEW_TASK لازم است
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        context.startActivity(intent)
                    }
                    Log.d(TAG, "Settings activity for MANAGE_ALL_FILES opened.")
                    // توجه: نتیجه این درخواست مستقیماً به برنامه برنمی‌گردد.
                    // باید دوباره Environment.isExternalStorageManager() را چک کنید
                    // وقتی کاربر به برنامه برمی‌گردد (مثلاً در onResume اکتیویتی).

                } catch (e: ActivityNotFoundException) {
                    // اگر صفحه تنظیمات مربوطه در دستگاه وجود نداشت (بسیار نادر)
                    Log.e(TAG, "Activity not found to handle MANAGE_ALL_FILES_ACCESS_PERMISSION intent.", e)
                    // می‌توانید یک Intent عمومی‌تر برای تنظیمات برنامه امتحان کنید
                    // val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                    // intent.data = Uri.parse("package:${context.packageName}")
                    // context.startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                } catch(t: Throwable) {
                     Log.e(TAG, "Error opening MANAGE_ALL_FILES settings", t)
                }
            } else {
                Log.d(TAG, "MANAGE_EXTERNAL_STORAGE permission already granted.")
                // اگر مجوز از قبل داده شده، کاری انجام نمی‌دهیم
            }
        } else {
            // برای نسخه‌های پایین‌تر از اندروید 11، این مجوز وجود ندارد
            Log.w(TAG, "MANAGE_EXTERNAL_STORAGE permission is not applicable below Android 11 (API 30).")
        }
    }

    // --- متدهای کمکی دیگر (می‌توانید اضافه کنید) ---

    /**
     * بررسی می‌کند آیا مجوزهای استاندارد ذخیره‌سازی داده شده‌اند یا نه.
     */
    @JvmStatic
    fun hasStoragePermissions(context: Context): Boolean {
         val readPermission = ContextCompat.checkSelfPermission(context, Manifest.permission.READ_EXTERNAL_STORAGE)
         val writePermission = ContextCompat.checkSelfPermission(context, Manifest.permission.WRITE_EXTERNAL_STORAGE)
         return readPermission == PackageManager.PERMISSION_GRANTED && writePermission == PackageManager.PERMISSION_GRANTED
    }

     /**
     * بررسی می‌کند آیا مجوز مدیریت تمام فایل‌ها داده شده است (فقط اندروید ۱۱ به بالا).
     */
    @JvmStatic
    @RequiresApi(Build.VERSION_CODES.R)
    fun hasManageAllFilesPermission(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
             Environment.isExternalStorageManager()
         } else {
             // در نسخه‌های پایین‌تر، این مجوز وجود ندارد، پس true برمی‌گردانیم؟
             // یا false چون مفهوم ندارد؟ بستگی به منطق برنامه دارد.
             // معمولا true مناسب‌تر است چون محدودیت وجود ندارد.
             true // یا false بر اساس نیاز
         }
    }

}