// CTest2.java
import static org.junit.Assert.assertEquals;
import org.junit.Before;
import org.junit.After;
import org.junit.Test;

public class CTest2 {
  private C c;

  @Before public void setUp() {
    System.out.println("setUp()");
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
  @After public void tearDown() {
    System.out.println("tearDown()");
  }
}

// > java org.junit.runner.JUnitCore CTest2 
// JUnit version 4.2
// .setUp()
// tearDown()
// .setUp()
// tearDown()
//
// Time: 0.11
// OK (2 tests)
