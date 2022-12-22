//#include <LiquidCrystal_PCF8574.h>
//#include <Wire.h>
//
//LiquidCrystal_PCF8574 lcd(0x27); 
//// set the LCD address to 0x27 
//
//void setup()
//{
//  lcd.begin(16, 2); // initialize the lcd  
//} // setup()
//
//void loop(){   
//    lcd.setBacklight(80);         // 調整背光
//    lcd.home();                   // 重製LCD
//    lcd.clear();                  // 清除螢幕顯示字
//    lcd.setCursor(0, 0);          // 設定游標位置到(0,0)，第0行第0個位置
//    lcd.print("HELLO WORLD!!!");  // 顯示字
//    lcd.s)etCursor(0, 1;          // 設定游標位置為(0,1),第1行第0個位置
//    delay(2100);                  // 延遲 2100ms
//} // loop()

//
#define LED 7
#define LED_RED 6
#define BEEPER 3
#include <Wire.h> // I2C程式庫
#include <LiquidCrystal_I2C.h> // LCD_I2C模組程式庫

// LCD I2C位址，默認為0x27或0x3F，依據背板的晶片不同而有差異，16、2為LCD顯示器大小。
LiquidCrystal_I2C lcd(0x27, 16, 2); 
String str;
void setup() {
  pinMode(LED, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BEEPER, OUTPUT);
  // 初始化LCD
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
}
void loop() {

  if (Serial.available()) {
    str = Serial.readStringUntil('\n');
    if (str == "LCD_SHOW_a"){
      lcd.clear();         // 清除螢幕顯示字
      lcd.setCursor(0, 0); // (colum, row)從第一排的第1個位置開始顯示
      lcd.print("Disinfecting"); 
      lcd.setCursor(0, 1); // (colum,row)從第二排第1格位置開始顯示
      lcd.print("No Person");
      digitalWrite(LED, HIGH); // 開燈
      digitalWrite(LED_RED, LOW); // 開燈red
      Serial.println("LED is ON"); // 回應訊息給電腦
      digitalWrite(BEEPER, LOW);
      delay(1000); // stop 1 sec
    }
    else if(str == "LCD_SHOW_b")
    {
      lcd.clear();         // 清除螢幕顯示字
      lcd.setCursor(0, 0); // (colum, row)從第一排的第三個位置開始顯示
      lcd.print("Detect Person"); 
      lcd.setCursor(0, 1); // (c！！olum,row)從第二排第三格位置開始顯示
      lcd.print("Please keep away");
      digitalWrite(LED, LOW);
      digitalWrite(LED_RED, HIGH); // 開燈red
      Serial.println("LED is OFF");
      digitalWrite(BEEPER, HIGH);
      delay(3000); // beep 3 sec
    }
  }
}

//#define LED 7
//String str;
//
//void setup() {
//  pinMode(LED, OUTPUT);
//  Serial.begin(9600);
//}
//
//void loop() {
//  if (Serial.available()) {
//    // 讀取傳入的字串直到"\n"結尾
//    str = Serial.readStringUntil('\n');
//
//    if (str == "LED_ON") {           // 若字串值是 "LED_ON" 開燈
//        digitalWrite(LED, HIGH);     // 開燈
//        Serial.println("LED is ON"); // 回應訊息給電腦
//    } else if (str == "LED_OFF") {
//        digitalWrite(LED, LOW);
//        Serial.println("LED is OFF");
//    }
//  }
//}
