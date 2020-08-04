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

    private int xCenter, yCenter;
    private static int OFFSET ;
    private static int MAX ;
    int percent ;

    private DrawCanvas draw;
    private Paint paint;

    private boolean touch_state = false;

    SwipeController(Context context, ViewGroup layout, int controller_res_id, boolean isVertical, int offset){
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

        OFFSET = offset;
        if (isVertical){
            MAX = layoutParams.height - OFFSET;
        } else {
            MAX = layoutParams.width - OFFSET;
        }
    }

    void setStickCenter(){
        draw.position(xCenter,yCenter);
        draw();
    }

    void setStickSize(int width, int height){
        stick = Bitmap.createScaledBitmap(stick,width,height,false);
        stick_width = stick.getWidth();
        stick_height = stick.getHeight();
    }

    private int calPostion(int point){
        int result;
        result = (point - OFFSET) * 100/(MAX - OFFSET) ;
        return result;
    }

    private void draw() {
        try {
            layout.removeView(draw);
        } catch (Exception e) {
            System.out.print("그냥..");
        }
        layout.addView(draw);
    }

    void drawStick(MotionEvent arg1) {

        if (isVertical){

            if(arg1.getAction() == MotionEvent.ACTION_DOWN) {   // stick touch
                draw.position(xCenter, arg1.getY());
                draw();
                touch_state = true;

            } else if(arg1.getAction() == MotionEvent.ACTION_MOVE && touch_state) { //stick move
                if(arg1.getY() >= MAX) {                                            //moving up
                    draw.position(xCenter,MAX);
                    percent = (MAX - OFFSET) * 100/(MAX - OFFSET);
                    draw();
                }else if (arg1.getY() <= OFFSET){                                   //moving down
                    draw.position(xCenter,OFFSET);
                    percent = calPostion(OFFSET);
                    draw();
                }else {                                                             //until MAX
                    draw.position(xCenter,arg1.getY());
                    percent = calPostion((int)arg1.getY());
                    draw();
                }

            } else if(arg1.getAction() == MotionEvent.ACTION_UP) {                  //end touch
                setStickCenter();
                percent = calPostion(yCenter);
                touch_state = false;
            }

        } else {

            if(arg1.getAction() == MotionEvent.ACTION_DOWN) {
                draw.position(arg1.getX(), yCenter);
                draw();
                touch_state = true;

            } else if(arg1.getAction() == MotionEvent.ACTION_MOVE && touch_state) {
                if(arg1.getX() >= MAX) {
                    draw.position(MAX, yCenter);
                    percent = (MAX - OFFSET) * 100/(MAX - OFFSET);
                    draw();
                }else if (arg1.getX() <= OFFSET){
                    draw.position(OFFSET, yCenter);
                    percent = calPostion(OFFSET);
                    draw();
                }else {
                    draw.position(arg1.getX(), yCenter);
                    percent = calPostion((int)arg1.getX());
                    draw();
                }

            } else if(arg1.getAction() == MotionEvent.ACTION_UP) {
                setStickCenter();
                percent = calPostion(xCenter);
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
            x = pos_x - (int)(stick_width / 2);
            y = pos_y - (int)(stick_height / 2);
        }
    }
}
