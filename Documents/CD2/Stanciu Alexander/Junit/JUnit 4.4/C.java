// C.java
// Application class under test. 	
// Normally, you don't need to test 
// very simple methods like set() or get().
// This example is only considered 
// for the sake of simplicity.  
public class C {
  private int i;
  private String s;

  public int getI() {
    return this.i;
  }
  public String getS() {
    return this.s;
  }
  public void setI(int ival) {
    this.i = ival;
  }
  public void setS(String sval) {
    this.s = sval;
  }
}
