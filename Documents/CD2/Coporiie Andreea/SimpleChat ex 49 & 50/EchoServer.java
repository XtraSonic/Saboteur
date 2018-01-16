// This file contains material supporting section 3.7 of the textbook:
// "Object Oriented Software Engineering" and is issued under the open-source
// license found at www.lloseng.com 

import java.io.*;

import common.ChatIF;
import ocsf.server.*;

/**
 * This class overrides some of the methods in the abstract 
 * superclass in order to give more functionality to the server.
 *
 * @author Dr Timothy C. Lethbridge
 * @author Dr Robert Lagani&egrave;re
 * @author Fran&ccedil;ois B&eacute;langer
 * @author Paul Holden
 * @version July 2000
 */
public class EchoServer extends AbstractServer 
{
  //Class variables *************************************************

  ChatIF serverUI;

  /**
   * The default port to listen on.
   */
  final public static int DEFAULT_PORT = 5555;

  public static final String SRV_PROMPT = "SERVER MSG>";
  //Constructors ****************************************************
  
  /**
   * Constructs an instance of the echo server.
   *
   * @param port The port number to connect on.
   */
  public EchoServer(int port, ChatIF serverUI)
  {
    super(port);
    this.serverUI = serverUI;
    serverUI.display("Welcome to Simple Chat server administration!");
  }

  
  //Instance methods ************************************************
  
  /**
   * This method handles any messages received from the client.
   *
   * @param msg The message received from the client.
   * @param client The connection from which the message originated.
   */
  public void handleMessageFromClient
    (Object msg, ConnectionToClient client)
  {
    System.out.println("Message received: " + msg + " from " + client);
    this.sendToAllClients(msg);
  }
    
  /**
   * This method overrides the one in the superclass.  Called
   * when the server starts listening for connections.
   */
  protected void serverStarted()
  {
    System.out.println
      ("Server listening for connections on port " + getPort());
  }
  
  /**
   * This method overrides the one in the superclass.  Called
   * when the server stops listening for connections.
   */
  protected void serverStopped()
  {
    System.out.println
      ("Server has stopped listening for connections.");
  }

    @Override
    protected void clientConnected(ConnectionToClient client) {
        System.out.println("Client " + client + " connected");
    }

    @Override
    protected synchronized void clientDisconnected(ConnectionToClient client) {
        System.out.println("Client "+ client + " disconnected");
    }

    @Override
    protected synchronized void clientException(ConnectionToClient client, Throwable exception) {
        System.out.println("Client " + client + " shut down");
    }



    /**
     * This method handles all data coming from the UI
     *
     * @param message The message from the UI
     */
    public void handleMessageFromServerUI(String message) {
        if (message.startsWith("#")){
            handleCommand(message);
        }else{
            sendToAllClients(SRV_PROMPT + message);
        }
    }

    /**
     * This method handles all commands coming from the UI
     *
     * @param command The command from the UI
     */
    private void handleCommand(String command) {
      if (command.matches("#quit")){
          sendToAllClients(SRV_PROMPT + "Terminating server.");
          serverUI.display("Terminating server.");
          this.quit();
          return;
      }
      if (command.matches("#stop")){
          sendToAllClients(SRV_PROMPT + "Server stopped listening.");
          serverUI.display("Server stopped listening");
          this.stopListening();
          return;
      }
      if (command.matches("#close")){
          sendToAllClients(SRV_PROMPT + "Server disconnecting.");
          serverUI.display("Server disconnecting");
          this.stopListening();
          try {
              this.close();
          } catch (IOException e) {
              serverUI.display("Error while disconnecting client");
          }
          return;
      }
      if (command.matches("#setport.*")){
          if (!command.matches("#setport\\s+\\d{4,6}?")){
              serverUI.display("Usage: #setport <port number>");
              return;
          }
          String[] split = command.split("\\s+");
          if (this.isListening()){
              serverUI.display("ERROR: Listening on " + this.getPort() + ", cannot change port");
              return;
          }
          if (split.length != 2){
              serverUI.display("ERROR: Could not resolve port.");
              return;
          }
          this.setPort(Integer.parseInt(split[1]));
          serverUI.display("New port: " + this.getPort());
          return;
      }
      if (command.matches("#start")){
          try {
              this.listen();
          } catch (IOException e) {
              serverUI.display("ERROR: Could not start server");
          }
          return;
      }
      if (command.matches("#getport")){
          serverUI.display("Port: " + this.getPort());
          return;
      }
      serverUI.display("Command not found: " + command);
    }

    private void quit() {
        try {
            this.stopListening();
            this.close();
        } catch (IOException e) {}
        System.exit(0);
    }
}
//End of EchoServer2 class
