// TSuite.java
import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
  ThreeCTest1.class,
  CTest2.class
})
public class TSuite {
}

//> java -ea org.junit.runner.JUnitCore TSuite
//JUnit version 4.2 
// .......setUp()
// tearDown()
// .setUp()
// tearDown()
//
// Time: 0.15
// OK (8 tests)
