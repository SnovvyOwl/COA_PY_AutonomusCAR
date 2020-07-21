package com.example.wirelesscontroller;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;

public class SwipeController {

    private Context context;
    private ViewGroup layout;
    private ViewGroup.LayoutParams layoutParams;
    private Bitmap stick;
    private boolean isVertical;
    private int stick_width, stick_height;

    private int xCenter = 0, yCenter = 0, min_distance = 0;
    public int percent = 0;
    private static int OFFSET = 0;
    private float distance = 0;

    private DrawCanvas draw;
    private Paint paint;

    private boolean touch_state = false;

    public SwipeController(Context context, ViewGroup layout, int controller_res_id, boolean isVertical){
        this.isVertical = isVertical;
        this.context = context;
        this.layout = layout;
        layoutParams = layout.getLayoutParams();

        stick = BitmapFactory.decodeResource(context.getResources(),controller_res_id);
        stick_width = stick.getWidth();
        stick_height = stick.getHeight();

        xCenter = layoutParams.width / 2;
        yCenter = layoutParams.height / 2;

        draw = new DrawCanvas(context);
        paint = new Paint();
    }

    public void setStickCenter(){
        draw.position(layoutParams.width/2,layoutParams.height/2);
        draw();
    }

    public void setStickSize(int width, int height){
        stick = Bitmap.createScaledBitmap(stick,width,height,false);
        stick_width = stick.getWidth();
        stick_height = stick.getHeight();
    }

    public void setOffset(int offset){
        OFFSET = offset;
    }

    private int calPostion(int point){
        int result;
        result = (point - OFFSET) * 100/(layoutParams.height - 2*OFFSET) ;
        return result;
    }

    private void draw() {
        try {
            layout.removeView(draw);
        } catch (Exception e) { }
        layout.addView(draw);
    }

    public void drawStick(MotionEvent arg1) {

        if (isVertical){
            int max = layoutParams.height - OFFSET;
            if(arg1.getAction() == MotionEvent.ACTION_DOWN) {
                draw.position(xCenter, arg1.getY());
                draw();
                touch_state = true;
            } else if(arg1.getAction() == MotionEvent.ACTION_MOVE && touch_state) {
                if(arg1.getY() >= (layoutParams.height) - OFFSET) {
                    draw.position(xCenter,max);
                    percent = (max - OFFSET) * 100/(max - OFFSET);
                    draw();
                }else if (arg1.getY() <= OFFSET){
                    draw.position(xCenter,OFFSET);
                    percent = calPostion(OFFSET);
                    draw();
                }else {
                    draw.position(xCenter,arg1.getY());
                    percent = calPostion((int)arg1.getY());
//                    percent = (int)((arg1.getY() - 90) * 100/(max - 90));
                    draw();
                }
            } else if(arg1.getAction() == MotionEvent.ACTION_UP) {
                setStickCenter();
                percent = calPostion(layoutParams.height/2);
//                percent = (int)((layoutParams.height/2 - OFFSET)* 100/(max - OFFSET));
                touch_state = false;
            }
        } else {
            if(arg1.getAction() == MotionEvent.ACTION_DOWN) {
                draw.position(arg1.getX(), yCenter);
                draw();
                touch_state = true;
            } else if(arg1.getAction() == MotionEvent.ACTION_MOVE && touch_state) {
                if(arg1.getX() >= (layoutParams.width) - OFFSET) {
                    draw.position(layoutParams.width - OFFSET, yCenter);
                    draw();
                }else if (arg1.getX() <= OFFSET){
                    draw.position(OFFSET, yCenter);
                    draw();
                }else {
                    draw.position(arg1.getX(), yCenter);
                    draw();
                }
            } else if(arg1.getAction() == MotionEvent.ACTION_UP) {
                setStickCenter();
                touch_state = false;
            }
        }
    }

    private class DrawCanvas extends View {
        float x, y;

        private DrawCanvas(Context mContext) {
            super(context);
        }

        public void onDraw(Canvas canvas) {
            canvas.drawBitmap(stick, x, y, paint);
        }

        private void position(float pos_x,  float pos_y) {
            x = pos_x - (stick_width / 2);
            y = pos_y - (stick_height / 2);
        }
    }

}
