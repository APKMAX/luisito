package org.luisito.myapp;

import android.app.Service;
import android.content.Intent;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

public class SumService extends Service {
    private Handler handler;
    private Runnable task;

    @Override
    public void onCreate() {
        super.onCreate();
        handler = new Handler();
        task = new Runnable() {
            @Override
            public void run() {
                int total = 0;
                for (int i = 1; i <= 100; i++) {
                    total += i;
                }
                Log.d("SumService", "Suma del 1 al 100: " + total);
                handler.postDelayed(this, 30000);
            }
        };
        handler.post(task);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY; // Mantener vivo el servicio
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        handler.removeCallbacks(task);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
