import static org.junit.Assert.*;

import org.junit.*;
import org.junit.Test;

// CTest1.java 
public class CTest1 {
  private C c;
	
  @Before public void setUp() {
    c = new C();
  }
  @Test public void testI() {
    int j = 10;
    c.setI(j);
    assertEquals(c.getI(),j);
  }
  @Test public void testS() {
    String t = "str";
    c.setS(t);
    assertEquals(c.getS(),t);
  }
}

// > java org.junit.runner.JUnitCore CTest1 
// JUnit version 4.2
// ..
// Time: 0.09
// OK (2 tests)
