const int trigPin = 7;
const int echoPin = 8;

void setup() {
  Serial.begin(9600); // 9600

  pinMode(trigPin, OUTPUT); // trig e pulse send
  pinMode(echoPin, INPUT);  // echo te pulse receive
}

void loop() {
  // age trig ke LOW kore ektu thamao
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // 10 ms er pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // echo HIGH thakar duration
  long duration = pulseIn(echoPin, HIGH, 30000);

  // somoy theke cm: sound speed 0.034 cm/us, jawa-asha tai 2 diye bhag
  int distance = duration * 0.034 / 2;

  Serial.println(distance);

  delay(30);  // sensor delay
}