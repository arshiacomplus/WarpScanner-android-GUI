package com.arshiacomplus.warpscanner.warpscanner // << پکیج نیم شما

import android.app.Activity
import android.content.pm.PackageManager
import android.util.Log
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import android.Manifest

object PermissionHelper { // <<<< باید object یا class باشد، نه چیز دیگر

    private const val TAG = "PermissionHelperKt"
    private const val STORAGE_PERMISSION_REQUEST_CODE = 101

    @Volatile
    private var permissionCallback: PermissionCallback? = null

    @JvmStatic
    fun requestStoragePermission(activity: Activity, callback: PermissionCallback) {
        Log.d(TAG, "requestStoragePermission called from Python")
        this.permissionCallback = callback

        val permissionsToRequest = arrayOf(
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
        )

        val permissionsNeeded = permissionsToRequest.filter {
            ContextCompat.checkSelfPermission(activity, it) != PackageManager.PERMISSION_GRANTED
        }.toTypedArray()

        if (permissionsNeeded.isEmpty()) {
            Log.d(TAG, "All storage permissions already granted.")
            try {
                callback.onPermissionResult(true)
            } catch (t: Throwable) {
                Log.e(TAG, "Error calling callback.onPermissionResult (permissions already granted)", t)
            } finally {
                this.permissionCallback = null
            }
        } else {
            Log.d(TAG, "Requesting permissions: ${permissionsNeeded.joinToString()}")
            ActivityCompat.requestPermissions(
                activity,
                permissionsNeeded,
                STORAGE_PERMISSION_REQUEST_CODE
            )
        }
    }

    @JvmStatic
    fun handleRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        Log.d(TAG, "handleRequestPermissionsResult called from MainActivity for requestCode: $requestCode")
        if (requestCode == STORAGE_PERMISSION_REQUEST_CODE) {
            val callback = this.permissionCallback
            if (callback != null) {
                val allGranted = grantResults.isNotEmpty() && grantResults.all { it == PackageManager.PERMISSION_GRANTED }
                Log.d(TAG, "Permission result: allGranted = $allGranted")
                try {
                    callback.onPermissionResult(allGranted)
                } catch (t: Throwable) {
                    Log.e(TAG, "Error calling callback.onPermissionResult (after request)", t)
                } finally {
                    this.permissionCallback = null
                    Log.d(TAG, "Permission callback cleared.")
                }
            } else {
                Log.w(TAG, "permissionCallback was null when handling result.")
            }
        } else {
             Log.w(TAG, "Received result for unknown requestCode: $requestCode")
        }
    }
}