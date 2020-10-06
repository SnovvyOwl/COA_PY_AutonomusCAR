package com.example.wirelesscontroller;

public class Car {

    private static int speed = 50;
    private static int direction = 50;

    static int cSpeed = 0;          //currentSpeed
    static int cDirection = 0;      //currentDirection

    public int getSpeed() {
        return speed;
    }

    public static void setSpeed(int speed) {
        Car.speed = speed;
    }

    public static int getDirection() {
        return direction;
    }

    public static void setDirection(int direction) {
        Car.direction = direction;
    }
}
