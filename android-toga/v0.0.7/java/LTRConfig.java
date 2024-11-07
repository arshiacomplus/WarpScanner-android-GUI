package org.beeware.android;

import android.app.Activity;
import android.os.Build;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;

public class LTRConfig {

    public static void applyLTR(Activity activity) {
        ViewGroup rootView = (ViewGroup) activity.findViewById(android.R.id.content);
        setLTR(rootView);
    }

    private static void setLTR(ViewGroup viewGroup) {
        for (int i = 0; i < viewGroup.getChildCount(); i++) {
            View view = viewGroup.getChildAt(i);
            if (view instanceof ViewGroup) {
                setLTR((ViewGroup) view);
            }
        }

        // اگر نسخه اندروید بالاتر از نوقا است، جهت LTR را تنظیم می‌کنیم
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            viewGroup.setLayoutDirection(View.LAYOUT_DIRECTION_LTR);
        }
    }
}
