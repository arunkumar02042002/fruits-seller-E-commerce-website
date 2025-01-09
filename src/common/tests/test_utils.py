from threading import current_thread

from django.test import TestCase

from common.utils import GlobalVariable

class TestGlobalVariable(TestCase):
    """Test GlobalVariable Feature."""

    def setUp(self):
        """Set up the GlobalVariable instance."""
        self.global_var = GlobalVariable()
    
    def test_set_and_get_val(self):
        """Test setting and getting a value."""
        self.global_var.set_val('test_attribute', 'test_value')
        self.assertEqual(
            self.global_var.get_val('test_attribute'),
            'test_value',
            "The value retrieved should match the value set."
        )
    
    def test_get_val_with_default(self):
        """Test getting a value with a default."""
        default_value = 'default_value'
        self.assertEqual(
            self.global_var.get_val('non_existent_attribute', default_value),
            default_value,
            "The default value should be returned for a non-existent attribute."
        )
    
    def test_cleanup_on_exit(self):
        """Test if attributes are cleaned up on exit."""
        with self.global_var as gv:
            gv.set_val('temp_attribute', 'temp_value')
            self.assertTrue(
                hasattr(current_thread(), 'temp_attribute'),
                "The thread should have the 'temp_attribute' set."
            )
        
        # After exiting the context manager
        self.assertFalse(
            hasattr(current_thread(), 'temp_attribute'),
            "The 'temp_attribute' should be removed after the context manager exits."
        )
    
    def test_multiple_attributes(self):
        """Test setting and cleaning up multiple attributes."""
        with self.global_var as gv:
            gv.set_val('attribute_1', 'value_1')
            gv.set_val('attribute_2', 'value_2')
            self.assertEqual(gv.get_val('attribute_1'), 'value_1')
            self.assertEqual(gv.get_val('attribute_2'), 'value_2')
        
        # Ensure both attributes are cleaned up
        self.assertFalse(hasattr(current_thread(), 'attribute_1'))
        self.assertFalse(hasattr(current_thread(), 'attribute_2'))
    
    def test_set_existing_attribute(self):
        """Test overwriting an existing attribute."""
        self.global_var.set_val('test_attribute', 'original_value')
        self.global_var.set_val('test_attribute', 'new_value')
        self.assertEqual(
            self.global_var.get_val('test_attribute'),
            'new_value',
            "The attribute value should be updated to the latest value."
        )
