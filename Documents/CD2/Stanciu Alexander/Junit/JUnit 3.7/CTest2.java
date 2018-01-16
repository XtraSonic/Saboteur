// CTest2.java

import junit.framework.TestCase;

public class CTest2 extends TestCase {
  private C c;

  public CTest2(String str) {
    super(str);
  }
  public void setUp() {
    System.out.println("setUp()");
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
  public void tearDown() {
    System.out.println("tearDown()");
  }
}

//> java junit.textui.TestRunner CTest2 
//.setUp()
//tearDown()
//.setUp()
//tearDown()
//
//Time: 0.03
//OK (2 tests)
