using AzureIoTHubDevices;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Client.Subscribing;
using MQTTnet.Protocol;
using System;
using System.Text;
using System.Threading.Tasks;

namespace subscribe
{
    class Program
    {
        static string cs = Environment.GetEnvironmentVariable("CS");
        static async Task Main(string[] args)
        {
            IMqttClient mqttClient = await IoTHubClient.CreateFromConnectionStringAsync(cs);
            mqttClient.UseApplicationMessageReceivedHandler(MessageReceived);

            var subRes = await mqttClient.SubscribeAsync("sample/topic", 
                                                            MqttQualityOfServiceLevel.AtMostOnce);
            
            Console.WriteLine("Subscribed. " + subRes.Items.Count);
            Console.ReadLine();
        }

        private static void MessageReceived(MqttApplicationMessageReceivedEventArgs arg)
        {
            string msg = Encoding.UTF8.GetString(arg.ApplicationMessage.Payload);
            Console.WriteLine(msg);
        }
    }
}
