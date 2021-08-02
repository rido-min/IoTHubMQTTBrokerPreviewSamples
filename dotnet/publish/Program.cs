using System;
using System.Text;
using System.Threading.Tasks;
using AzureIoTHubDevices;
using MQTTnet;
using MQTTnet.Client;

namespace publish
{
    class Program
    {
        static string cs = Environment.GetEnvironmentVariable("CS");

        static async Task Main(string[] args)
        {
            var mqttClient = await IoTHubClient.CreateFromConnectionStringAsync(cs);

            // az iot hub topic-space create --topic-name "SampleZero" --topic-template "sample/#" --type "LowFanout"
            var mqttMessage = new MqttApplicationMessage()
            {
                Topic = "sample/topic",
                Payload = Encoding.UTF8.GetBytes("<message-payload>"),
                QualityOfServiceLevel = 0
            };

            await mqttClient.PublishAsync(mqttMessage);

            Console.WriteLine("Message Published");
            Console.ReadLine();
        }
    }
}
