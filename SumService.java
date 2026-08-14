package org.example.myapp;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

public class SumService extends Service {
    private Handler handler;
    private Runnable task;
    private static final String CHANNEL_ID = "SumServiceChannel";

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
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "Sum Service Channel",
                NotificationManager.IMPORTANCE_DEFAULT
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);

            Notification notification = new Notification.Builder(this, CHANNEL_ID)
                .setContentTitle("SumService activo")
                .setContentText("Sumando cada 30 segundos...")
                .setSmallIcon(android.R.drawable.ic_media_play)
                .build();

            startForeground(1, notification);
        }
        return START_STICKY;
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
