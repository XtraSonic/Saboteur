// This file contains material supporting section 3.7 of the textbook:
// "Object Oriented Software Engineering" and is issued under the open-source
// license found at www.lloseng.com 

package client;

import ocsf.client.*;
import common.*;
import ocsftester.ClientFrame;

import java.io.*;

/**
 * This class overrides some of the methods defined in the abstract
 * superclass in order to give more functionality to the client.
 *
 * @author Dr Timothy C. Lethbridge
 * @author Dr Robert Lagani&egrave;
 * @author Fran&ccedil;ois B&eacute;langer
 * @version July 2000
 */
public class ChatClient extends AbstractClient
{
  //Instance variables **********************************************
  
  /**
   * The interface type variable.  It allows the implementation of 
   * the display method in the client.
   */
  ChatIF clientUI; 

  
  //Constructors ****************************************************
  
  /**
   * Constructs an instance of the chat client.
   *
   * @param host The server to connect to.
   * @param port The port number to connect on.
   * @param clientUI The interface type variable.
   */
  
  public ChatClient(String host, int port, ChatIF clientUI) 
    throws IOException 
  {
    super(host, port); //Call the superclass constructor
    this.clientUI = clientUI;
    clientUI.display("Welcome to Simple Chat!");
    //openConnection();
  }

  
  //Instance methods ************************************************
    
  /**
   * This method handles all data that comes in from the server.
   *
   * @param msg The message from the server.
   */
  public void handleMessageFromServer(Object msg) 
  {
    clientUI.display(msg.toString());
  }

  /**
   * This method handles all data coming from the UI            
   *
   * @param message The message from the UI.    
   */
  public void handleMessageFromClientUI(String message)
  {
    try
    {
        if (message.startsWith("#")){
            handleCommand(message);
        }else {
            sendToServer(message);
        }
    }
    catch(IOException e)
    {
      clientUI.display
        ("Could not send message to server.  Terminating client.");
      quit();
    }
  }

    /**
     * This method handles all commands coming from the UI
     *
     * @param command The command from the UI
     */
    private void handleCommand(String command) throws IOException {
        if (command.matches("#quit")){
            clientUI.display("Terminating client.");
            this.quit();
            return;
        }
        if (command.matches("#logoff")){
            clientUI.display("Logging off.");
            this.closeConnection();
            return;
        }
        if (command.matches("#sethost.*")){
            if (!command.matches("#sethost\\s+\\w+")){
                clientUI.display("Usage: #sethost <host name>");
                return;
            }
            String[] split = command.split("\\s+");
            if (this.isConnected()){
                clientUI.display("ERROR: Connected to " + this.getHost() + ":" + this.getPort() + ", cannot change host");
                return;
            }
            if (split.length != 2){
                clientUI.display("ERROR: Could not resolve host");
                return;
            }
            this.setHost(split[1]);
            clientUI.display("New host: " + this.getHost());
            return;
        }
        if (command.matches("#setport.*")){
            if (!command.matches("#setport\\s+\\d{4,6}?")){
                clientUI.display("Usage: #setport <port number>");
                return;
            }
            String[] split = command.split("\\s+");
            if (this.isConnected()){
                clientUI.display("ERROR: Connected to " + this.getHost() + ":" + this.getPort() + ", cannot change port");
                return;
            }
            if (split.length != 2){
                clientUI.display("ERROR: Could not resolve port");
                return;
            }
            this.setPort(Integer.parseInt(split[1]));
            clientUI.display("New port: " + this.getPort());
            return;
        }
        if (command.matches("#login")){
            if (this.isConnected()){
                clientUI.display("ERROR: Already connected to " + this.getHost() + ":" + this.getPort() + ", cannot log in");
                return;
            }
            clientUI.display("Connecting to " + this.getHost() + ":" + this.getPort());
            this.openConnection();
            return;
        }
        if (command.matches("#gethost")){
            clientUI.display("Host: " + this.getHost());
            return;
        }
        if (command.matches("#getport")){
            clientUI.display("Port: " + this.getPort());
            return;
        }
        clientUI.display("Command not found: " + command);
    }

    @Override
  protected void connectionClosed() {
    clientUI.display("The connection has closed");
  }

    @Override
    protected void connectionException(Exception exception) {
        clientUI.display("The server has shut down");
        quit();
    }

    /**
   * This method terminates the client.
   */
  public void quit()
  {
    try
    {
      closeConnection();
    }
    catch(IOException e) {}
    System.exit(0);
  }
}
//End of ChatClient2 class
