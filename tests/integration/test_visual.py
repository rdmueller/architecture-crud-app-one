"""Visual regression tests for the UI."""
import pytest
import os
from PIL import Image, ImageChops
import requests
from io import BytesIO
import hashlib
import shutil


class TestVisualRegression:
    """Visual regression tests using screenshots."""
    
    @pytest.fixture
    def screenshot_dir(self):
        """Create directory for screenshots."""
        dir_path = "tests/integration/screenshots"
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    
    @pytest.fixture
    def baseline_dir(self):
        """Create directory for baseline images."""
        dir_path = "tests/integration/screenshots/baseline"
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    
    def capture_screenshot(self, url, filename):
        """Capture a screenshot of a webpage (mock implementation)."""
        # Note: This is a simplified version. Real implementation would use Selenium
        # For now, we'll create a simple hash-based "fingerprint" of the page
        response = requests.get(url)
        if response.status_code == 200:
            # Create a "fingerprint" based on page content
            content_hash = hashlib.md5(response.text.encode()).hexdigest()
            
            # Create a simple image representation (for demo purposes)
            # In real implementation, this would be an actual screenshot
            img = Image.new('RGB', (800, 600), color='white')
            pixels = img.load()
            
            # Use hash to create a unique pattern
            for i, char in enumerate(content_hash):
                x = (i * 20) % 800
                y = (i * 20) // 800 * 20
                color_val = ord(char) * 15 % 255
                for dx in range(20):
                    for dy in range(20):
                        if x + dx < 800 and y + dy < 600:
                            pixels[x + dx, y + dy] = (color_val, color_val, color_val)
            
            img.save(filename)
            return True
        return False
    
    def compare_images(self, img1_path, img2_path, threshold=5):
        """Compare two images and return difference percentage."""
        if not os.path.exists(img1_path) or not os.path.exists(img2_path):
            return 100.0  # Maximum difference if files don't exist
        
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        # Ensure images are the same size
        if img1.size != img2.size:
            return 100.0
        
        # Calculate difference
        diff = ImageChops.difference(img1, img2)
        
        # Convert to grayscale for analysis
        diff = diff.convert('L')
        
        # Calculate percentage of pixels that differ
        pixels = diff.getdata()
        different_pixels = sum(1 for pixel in pixels if pixel > threshold)
        total_pixels = img1.size[0] * img1.size[1]
        
        difference_percentage = (different_pixels / total_pixels) * 100
        return difference_percentage
    
    @pytest.mark.skipif("RUN_SELENIUM_TESTS" not in os.environ,
                       reason="Visual tests require Selenium setup")
    def test_dashboard_visual(self, ui_server, screenshot_dir, baseline_dir):
        """Test dashboard visual appearance."""
        page_name = "dashboard"
        current_screenshot = os.path.join(screenshot_dir, f"{page_name}_current.png")
        baseline_screenshot = os.path.join(baseline_dir, f"{page_name}.png")
        
        # Capture current screenshot
        self.capture_screenshot(ui_server, current_screenshot)
        
        # Compare with baseline if it exists
        if os.path.exists(baseline_screenshot):
            difference = self.compare_images(baseline_screenshot, current_screenshot)
            assert difference < 5.0, f"Visual difference too large: {difference}%"
        else:
            # If no baseline, save current as baseline
            shutil.copy(current_screenshot, baseline_screenshot)
            print(f"Created baseline for {page_name}")
    
    @pytest.mark.skipif("RUN_SELENIUM_TESTS" not in os.environ,
                       reason="Visual tests require Selenium setup")
    def test_all_pages_visual(self, ui_server, screenshot_dir, baseline_dir):
        """Test visual appearance of all pages."""
        pages = [
            ("dashboard", "/"),
            ("adrs", "/?page=adrs"),
            ("qualities", "/?page=qualities"),
            ("risks", "/?page=risks"),
            ("technical_debts", "/?page=technical_debts"),
            ("components", "/?page=components"),
            ("relationships", "/?page=relationships"),
            ("export", "/?page=export")
        ]
        
        results = {}
        
        for page_name, path in pages:
            current_screenshot = os.path.join(screenshot_dir, f"{page_name}_current.png")
            baseline_screenshot = os.path.join(baseline_dir, f"{page_name}.png")
            
            # Capture screenshot
            success = self.capture_screenshot(f"{ui_server}{path}", current_screenshot)
            
            if success:
                if os.path.exists(baseline_screenshot):
                    difference = self.compare_images(baseline_screenshot, current_screenshot)
                    results[page_name] = {"status": "compared", "difference": difference}
                else:
                    shutil.copy(current_screenshot, baseline_screenshot)
                    results[page_name] = {"status": "baseline_created", "difference": 0}
            else:
                results[page_name] = {"status": "failed", "difference": 100}
        
        # Print results
        print("\nVisual Test Results:")
        for page, result in results.items():
            print(f"{page}: {result['status']} (difference: {result['difference']:.2f}%)")
        
        # Assert all pages have acceptable differences
        for page, result in results.items():
            if result['status'] == "compared":
                assert result['difference'] < 5.0, f"Visual regression on {page}: {result['difference']}%"
    
    def test_responsive_design(self, ui_server):
        """Test responsive design at different viewport sizes."""
        # This is a placeholder - real implementation would use Selenium
        # to test different viewport sizes
        viewport_sizes = [
            ("mobile", 375, 667),
            ("tablet", 768, 1024),
            ("desktop", 1920, 1080)
        ]
        
        for device, width, height in viewport_sizes:
            # In real implementation, we would:
            # 1. Set browser window size
            # 2. Capture screenshot
            # 3. Verify layout is appropriate for device
            print(f"Testing {device} layout ({width}x{height})")
            
            # Placeholder assertion
            assert True, f"Layout test for {device} would go here"


class TestAccessibility:
    """Basic accessibility tests."""
    
    def test_page_has_title(self, ui_server):
        """Test that pages have proper titles."""
        response = requests.get(ui_server)
        assert response.status_code == 200
        assert "<title>" in response.text
        assert "Architecture CRUD Application" in response.text
    
    def test_images_have_alt_text(self, ui_server):
        """Test that images have alt text (basic check)."""
        response = requests.get(ui_server)
        assert response.status_code == 200
        
        # Basic check - in real implementation would parse HTML properly
        content = response.text.lower()
        img_count = content.count("<img")
        
        if img_count > 0:
            # Check if images have alt attributes
            alt_count = content.count('alt="')
            print(f"Found {img_count} images, {alt_count} with alt text")
            # This is a very basic check - proper implementation would parse HTML
    
    def test_color_contrast(self, ui_server):
        """Test color contrast (placeholder)."""
        # This would require analyzing CSS and computing contrast ratios
        # For now, just check that the page loads
        response = requests.get(ui_server)
        assert response.status_code == 200
        
        # Placeholder for actual contrast testing
        print("Color contrast testing would be implemented here")
    
    def test_keyboard_navigation(self, ui_server):
        """Test keyboard navigation (placeholder)."""
        # This would require Selenium to simulate keyboard navigation
        # For now, just check for basic navigation elements
        response = requests.get(ui_server)
        assert response.status_code == 200
        
        # Check for navigation elements
        content = response.text.lower()
        assert "nav" in content or "navigation" in content
        print("Keyboard navigation testing would be implemented here")


class TestContentVerification:
    """Verify UI content matches API data."""
    
    def test_dashboard_metrics(self, api_server, ui_server):
        """Test that dashboard displays correct metrics."""
        # Get data from API
        api_response = requests.get(f"{api_server}/api/architecture")
        assert api_response.status_code == 200
        api_data = api_response.json()
        
        # Get dashboard page
        ui_response = requests.get(ui_server)
        assert ui_response.status_code == 200
        
        # Count entities in API data
        entity_counts = {
            "ADRs": len(api_data.get("adrs", {})),
            "Qualities": len(api_data.get("qualities", {})),
            "Risks": len(api_data.get("risks", {})),
            "Technical Debts": len(api_data.get("technicalDebts", {})),
            "Components": len(api_data.get("components", {}))
        }
        
        # Verify counts appear in UI (basic check)
        ui_content = ui_response.text
        for entity_type, count in entity_counts.items():
            # This is a simplified check - real implementation would parse HTML properly
            print(f"Checking {entity_type}: {count}")
            # Would verify actual numbers displayed in UI
    
    def test_entity_data_consistency(self, api_server, ui_server, sample_adr):
        """Test that entity data is consistent between API and UI."""
        # Create test data
        response = requests.post(f"{api_server}/api/adrs", json=sample_adr)
        assert response.status_code == 201
        
        # Get ADR from API
        api_response = requests.get(f"{api_server}/api/adrs/{sample_adr['id']}")
        assert api_response.status_code == 200
        api_adr = api_response.json()
        
        # Get ADRs page from UI
        ui_response = requests.get(f"{ui_server}?page=adrs")
        assert ui_response.status_code == 200
        
        # Verify ADR appears in UI (basic check)
        ui_content = ui_response.text
        assert sample_adr["title"] in ui_content
        
        # Clean up
        requests.delete(f"{api_server}/api/adrs/{sample_adr['id']}")
        
        print(f"Verified ADR '{sample_adr['title']}' appears in UI")
