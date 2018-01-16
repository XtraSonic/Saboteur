/*
 * HashMapTest.java
 *
 * Created on September 16, 2001, 12:27 PM
 */

import java.util.Map;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import java.util.HashMap;

/**
 *
 * @author  Rick Hightower
 * @version 1.0
 */

//The purpose of this class is to create a unit test for the Java
//Map class. It has several methods used to test the various methods and 
//properties of the Map class.

public class HashMapTest extends TestCase {

    private Map testMap;
    private Map testMap2;

    //Create a new TestCase    
    public HashMapTest(String name) {
        super(name);
    }

    //Create a new TestSuite
    public static Test suite() {
          return new TestSuite(HashMapTest.class);
    }
    
    //Run a new TestSuite in text mode
    public static void main (String[] args) {
         junit.textui.TestRunner.run (suite());
    }
    
    //Constants- key and value pairs for the APPLE_KEY and APPLE_VALUE
    private static final String APPLE_KEY = "AppleCEO";
    private static final String APPLE_VALUE = "AppleCEO";
    
    //The set up method does just as the name suggests- it sets up 
    //anything that the test needs to run, such as instantiating objects 
    //and setting values.

    protected void setUp() {
        //Create and populate two new HashMaps to have tests run on
        testMap = new HashMap();
        testMap.put(APPLE_KEY, APPLE_VALUE);
        testMap.put("OracleCEO","Larry Ellison");
        
        testMap2 = new HashMap();
        testMap2.put("1", "1");
        testMap2.put("2", "2");
        
    }
    
    //This method tests the Map's put method by adding Hightower to the
    //hash and then retrieving his key in order to verify that he was
    //added. It then asserts that the value retrieved for his key should
    //be equal to the value inserted.
    public void testPut(){
        String key = "Employee";
        String value = "Rick Hightower"; 
        
                //put the value in
        testMap.put(key, value);
        
                //read the value back out
        String value2 = (String)testMap.get(key);
        assertEquals("The value back from the map ", value, value2);
    }
    
    //This method checks that the size of the hash is correct.
    //It asserts that the size of testMap should be 2.
    public void testSize(){
        assertEquals (2, testMap.size());
    }
    
    //This method checks the get method. It first verifies that
    //when retrieving the APPLE_KEY the correct value is returned.
    //It then asserts that any value for a non-existant key should
    //be null.
    public void testGet(){
        assertEquals(APPLE_VALUE, testMap.get(APPLE_KEY));
        assertNull(testMap.get("JUNK_KEY"));
    }
    
    //This method tests the put all method. It inserts all of the
    //contents of testMap2 into testMap and then asserts that the
    //size should be 4 and that the value of key "1" should be 1
    public void testPutAll(){
        testMap.putAll(testMap2);
        assertEquals (4, testMap.size());
        assertEquals("1", testMap.get("1"));
        testGet();
    }
    
    //This method tests the containsKey method. It asserts that the
    //Apple key should be in the map.
    public void testContainsKey(){
        assertTrue("It should contain the apple key", testMap.containsKey(APPLE_KEY));
    }

    //This method tests the containsValue method. It asserts that the
    //Apple value should be in the map.
    public void testContainsValue(){
        assertTrue(testMap.containsValue(APPLE_VALUE));
    }
    
    //This method tests the remove method. It inserts Hightower into
    //the hash, removes his key, and then asserts that any attempt to
    //retrieve his information should return as null.
    public void testRemove(){
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

