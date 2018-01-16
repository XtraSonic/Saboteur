// TSuite.java
import junit.framework.*;

public class TSuite {
  public static Test suite() {
    TestSuite suite2 = new TestSuite();
    TestSuite suite = new TestSuite();
    suite2.addTestSuite(CTest1.class);
    suite2.addTestSuite(CTest1.class);
    suite2.addTestSuite(CTest1.class);
    suite.addTest(suite2);
    suite.addTestSuite(CTest2.class);
    return suite;
  }

  public static void main(String[] args)  
  {
    junit.textui.TestRunner.run(suite());
  }
}

// > java TSuite
// .......setUp()
// tearDown()
// .setUp()
// tearDown()
//
// Time: 0.04
// OK (8 tests)
