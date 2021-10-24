#include "mbed.h"
#include "C12832.h"


C12832 lcd(p5, p7, p6, p8, p11);

int main()
{
    float j=0.0;
    lcd.cls();
    lcd.locate(0,3);
    lcd.printf("This is team HackEye!");

    while(true) {   // this is the third thread
        lcd.locate(0,15);
        lcd.printf("Counting : %.1f",j);
        j = j + 0.25;
        wait(0.25);
    }
}
