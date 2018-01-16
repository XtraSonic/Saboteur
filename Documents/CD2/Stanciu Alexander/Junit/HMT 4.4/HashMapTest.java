import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.Map;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;

public class HashMapTest {
	private Map testMap;
    private Map testMap2;
    
    private static final String APPLE_KEY = "AppleCEO";
    private static final String APPLE_VALUE = "AppleCEO";
    
    @Before public void setUp() {
        //Create and populate two new HashMaps to have tests run on
        testMap = new HashMap();
        testMap.put(APPLE_KEY, APPLE_VALUE);
        testMap.put("OracleCEO","Larry Ellison");
        
        testMap2 = new HashMap();
        testMap2.put("1", "1");
        testMap2.put("2", "2");
        
    }
    
    @Test public void testPut(){
        String key = "Employee";
        String value = "Rick Hightower"; 
        
                //put the value in
        testMap.put(key, value);
        
                //read the value back out
        String value2 = (String)testMap.get(key);
        assertEquals("The value back from the map ", value, value2);
    }
    
    @Test public void testSize(){
        assertEquals (2, testMap.size());
    }
    
    @Test public void testGet(){
        assertEquals(APPLE_VALUE, testMap.get(APPLE_KEY));
        assertNull(testMap.get("JUNK_KEY"));
    }
    
    @Test public void testPutAll(){
        testMap.putAll(testMap2);
        assertEquals (4, testMap.size());
        assertEquals("1", testMap.get("1"));
        testGet();
    }
    
    @Test public void testContainsKey(){
        assertTrue("It should contain the apple key", testMap.containsKey(APPLE_KEY));
    }

    @Test public void testContainsValue(){
        assertTrue(testMap.containsValue(APPLE_VALUE));
    }
    
    @Test public void testRemove(){
        String key = "Employee";
        String value = "Rick Hightower"; 
        
                //put the value in
        testMap.put(key, value);
        
                //remove it
        testMap.remove(key);
        
                //try to read the value back out
        assertNull(testMap.get(key));

    }
}
