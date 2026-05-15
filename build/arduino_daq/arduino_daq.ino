/*
 * Firmware for turning and Arduino into a simple data acquisition (DAQ) module.
 * (c)2026 Copyright LilyTronics
 *
 * Serial commands:
 *   id     : returns the ID string 'Arduino DAQ'
 *   rax    : read analog input; x is analog input number
 *   rdx    : read digital state; x is the digital IO number
 *   six    : set digital input; x is the digital IO number
 *   wdx s  : write digital output; x is the digital IO number; s is the state (0/1)
 *
 * Example:
 *
 *   Open serial port at 115200 baud.
 *
 *   Read ID:
 *   TX: id\n
 *   RX: Arduino DAQ\n
 *
 *   Read analog:
 *   TX: ra2\n
 *   RX: 4.286\n
 *
 *   Digital read and write
 *   Default all are input
 *   TX: rd4\n
 *   RX: 0\n
 *   To make a pin output, simply write a state
 *   TX: wd3 1
 *   RX: ok\n
 *   Once a pin is output, the output state can be read back
 *   TX: rd3\n
 *   RX: 1\n
 *   Reset pin to input
 *   TX: si3\n
 *   RX: ok\n
 *
 */

#define BOARD_NAME      "Arduino DAQ"
#define TERMINATION     '\n'

// Analog channels
#define ANALOG_MIN      0
#define ANALOG_MAX      5

// Digital channels (0 and 1 are reserved for the UART)
#define DIGITAL_MIN     2
#define DIGITAL_MAX     13

String rx_data;

void setup()
{
    // Define all as inputs (save)
    for (int i = DIGITAL_MIN; i <= DIGITAL_MAX; i++)
    {
        pinMode(i, INPUT);
    }
    Serial.begin(115200);
}

void loop()
{
    if (Serial.available() > 0)
    {
        rx_data = Serial.readStringUntil(TERMINATION);

        // ID string
        if (rx_data == "id")
        {
            Serial.print(BOARD_NAME);
            Serial.print(TERMINATION);
        }

        // Analog channel
        else if (rx_data.startsWith("ra"))
        {
            int channel = rx_data.substring(2).toInt();
            if (channel >= ANALOG_MIN && channel <= ANALOG_MAX)
            {
                Serial.print(analogRead(channel + A0) * 5.0 / 1023, 3);
                Serial.print(TERMINATION);
            }
        }

        // Digital read
        else if (rx_data.startsWith("rd"))
        {
            // Read digital
            int channel = rx_data.substring(2).toInt();
            if (channel >= DIGITAL_MIN && channel <= DIGITAL_MAX)
            {
                Serial.print(digitalRead(channel));
                Serial.print(TERMINATION);
            }
        }

        // Digital write
        else if (rx_data.startsWith("wd"))
        {
            int space_index = rx_data.indexOf(' ');
            if (space_index > 2)
            {
                int channel = rx_data.substring(2, space_index).toInt();
                if (channel >= DIGITAL_MIN && channel <= DIGITAL_MAX)
                {
                    int value = rx_data.substring(space_index).toInt();
                    if (value == 0 || value == 1)
                    {
                        pinMode(channel, OUTPUT);
                        digitalWrite(channel, value);
                        Serial.print("ok");
                        Serial.print(TERMINATION);
                    }
                }
            }
        }

        // Set pin to input
        else if (rx_data.startsWith("si"))
        {
            int channel = rx_data.substring(2).toInt();
            if (channel >= DIGITAL_MIN && channel <= DIGITAL_MAX)
            {
                pinMode(channel, INPUT);
                Serial.print("ok");
                Serial.print(TERMINATION);
            }
        }
    }
}
