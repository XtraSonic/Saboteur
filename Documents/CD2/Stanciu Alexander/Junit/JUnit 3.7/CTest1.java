// CTest1.java
import junit.framework.TestCase;

public class CTest1 extends TestCase {
  private C c;
	
  // Creates a test case and sets its
  // name to arg.
  // Since JUnit 3.8.1 you 
  // don't need to override this 
  // constructor in subclasses 
  // of TestCase.
  public CTest1(String arg) {
    super(arg);
  }
  public void setUp() {
    c = new C();
  }
  public void testI() {
    int j = 10;
    c.setI(j);
    assertEquals(c.getI(),j);
  }
  public void testS() {
    String t = "str";
    c.setS(t);
    assertEquals(c.getS(),t);
  }
}

// > java junit.textui.TestRunner CTest1 
// ..
// Time: 0.02
// OK (2 tests)
