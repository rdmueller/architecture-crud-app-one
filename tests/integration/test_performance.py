"""Performance tests for the Architecture CRUD Application."""
import pytest
import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import json


class TestAPIPerformance:
    """Test API performance under load."""
    
    def test_single_request_latency(self, api_server, sample_adr):
        """Test single request latency for different endpoints."""
        endpoints = [
            (f"{api_server}/health", "GET"),
            (f"{api_server}/api/architecture", "GET"),
            (f"{api_server}/api/adrs", "POST", sample_adr),
        ]
        
        results = {}
        
        for endpoint_data in endpoints:
            url = endpoint_data[0]
            method = endpoint_data[1]
            data = endpoint_data[2] if len(endpoint_data) > 2 else None
            
            # Warm up
            if method == "GET":
                requests.get(url)
            else:
                requests.post(url, json=data)
            
            # Measure
            times = []
            for _ in range(10):
                start = time.time()
                if method == "GET":
                    response = requests.get(url)
                else:
                    response = requests.post(url, json=data)
                end = time.time()
                
                if response.status_code in [200, 201]:
                    times.append((end - start) * 1000)  # Convert to ms
            
            results[url] = {
                "min": min(times),
                "max": max(times),
                "avg": statistics.mean(times),
                "median": statistics.median(times),
                "stdev": statistics.stdev(times) if len(times) > 1 else 0
            }
        
        # Print results
        print("\nSingle Request Latency Results (ms):")
        for url, metrics in results.items():
            print(f"\n{url}:")
            print(f"  Min: {metrics['min']:.2f}ms")
            print(f"  Max: {metrics['max']:.2f}ms")
            print(f"  Avg: {metrics['avg']:.2f}ms")
            print(f"  Median: {metrics['median']:.2f}ms")
            print(f"  StdDev: {metrics['stdev']:.2f}ms")
        
        # Assert reasonable performance
        for url, metrics in results.items():
            assert metrics['avg'] < 200, f"Average latency too high for {url}"
            assert metrics['max'] < 500, f"Max latency too high for {url}"
    
    def test_concurrent_requests(self, api_server, clean_storage):
        """Test API performance under concurrent load."""
        num_threads = 10
        requests_per_thread = 5
        
        def make_request(thread_id, request_id):
            """Make a single request."""
            adr_data = {
                "id": f"ADR-{thread_id:03d}-{request_id:03d}",
                "title": f"Test ADR {thread_id}-{request_id}",
                "status": "proposed",
                "date": "2024-01-01",
                "authors": [f"Thread {thread_id}"],
                "context": "Performance test",
                "decision": "Test decision",
                "alternatives": {},
                "relationships": {
                    "qualities": [],
                    "risks": [],
                    "technicalDebts": [],
                    "components": [],
                    "relatedAdrs": []
                }
            }
            
            start = time.time()
            response = requests.post(f"{api_server}/api/adrs", json=adr_data)
            end = time.time()
            
            return {
                "thread_id": thread_id,
                "request_id": request_id,
                "status_code": response.status_code,
                "duration": (end - start) * 1000  # ms
            }
        
        # Run concurrent requests
        results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for thread_id in range(num_threads):
                for request_id in range(requests_per_thread):
                    futures.append(
                        executor.submit(make_request, thread_id, request_id)
                    )
            
            for future in as_completed(futures):
                results.append(future.result())
        
        end_time = time.time()
        total_duration = (end_time - start_time) * 1000  # ms
        
        # Analyze results
        successful_requests = [r for r in results if r['status_code'] == 201]
        failed_requests = [r for r in results if r['status_code'] != 201]
        
        latencies = [r['duration'] for r in successful_requests]
        
        print(f"\nConcurrent Request Results:")
        print(f"Total requests: {len(results)}")
        print(f"Successful: {len(successful_requests)}")
        print(f"Failed: {len(failed_requests)}")
        print(f"Total duration: {total_duration:.2f}ms")
        print(f"Requests per second: {len(results) / (total_duration / 1000):.2f}")
        
        if latencies:
            print(f"\nLatency statistics (ms):")
            print(f"Min: {min(latencies):.2f}")
            print(f"Max: {max(latencies):.2f}")
            print(f"Avg: {statistics.mean(latencies):.2f}")
            print(f"Median: {statistics.median(latencies):.2f}")
            print(f"95th percentile: {sorted(latencies)[int(len(latencies) * 0.95)]:.2f}")
        
        # Assert performance criteria
        assert len(successful_requests) >= len(results) * 0.95, "Too many failed requests"
        if latencies:
            assert statistics.mean(latencies) < 500, "Average latency too high under load"
            assert sorted(latencies)[int(len(latencies) * 0.95)] < 1000, "95th percentile too high"
    
    def test_large_data_handling(self, api_server, clean_storage):
        """Test API performance with large data payloads."""
        # Create a large ADR with many relationships
        num_relationships = 50
        
        large_adr = {
            "id": "ADR-LARGE",
            "title": "Large ADR for Performance Testing",
            "status": "accepted",
            "date": "2024-01-01",
            "authors": ["Performance Tester"],
            "context": "Testing with large data " * 100,  # Large text
            "decision": "Decision text " * 100,  # Large text
            "alternatives": {
                f"Alternative-{i}": {
                    "pros": [f"Pro {j}" for j in range(10)],
                    "cons": [f"Con {j}" for j in range(10)]
                } for i in range(10)
            },
            "relationships": {
                "qualities": [
                    {
                        "id": f"Q-{i:03d}",
                        "type": "addresses",
                        "strength": "medium"
                    } for i in range(num_relationships)
                ],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        # Measure creation time
        start = time.time()
        response = requests.post(f"{api_server}/api/adrs", json=large_adr)
        create_time = (time.time() - start) * 1000
        
        assert response.status_code == 201, f"Failed to create large ADR: {response.text}"
        
        # Measure retrieval time
        start = time.time()
        response = requests.get(f"{api_server}/api/adrs/ADR-LARGE")
        get_time = (time.time() - start) * 1000
        
        assert response.status_code == 200
        
        # Measure update time
        large_adr["title"] = "Updated Large ADR"
        start = time.time()
        response = requests.put(f"{api_server}/api/adrs/ADR-LARGE", json=large_adr)
        update_time = (time.time() - start) * 1000
        
        assert response.status_code == 200
        
        # Measure architecture retrieval time
        start = time.time()
        response = requests.get(f"{api_server}/api/architecture")
        arch_time = (time.time() - start) * 1000
        
        assert response.status_code == 200
        
        print(f"\nLarge Data Performance Results:")
        print(f"Create time: {create_time:.2f}ms")
        print(f"Get time: {get_time:.2f}ms")
        print(f"Update time: {update_time:.2f}ms")
        print(f"Architecture retrieval time: {arch_time:.2f}ms")
        
        # Assert reasonable performance even with large data
        assert create_time < 1000, "Create time too high for large data"
        assert get_time < 500, "Get time too high for large data"
        assert update_time < 1000, "Update time too high for large data"
        assert arch_time < 2000, "Architecture retrieval too slow with large data"


class TestUIPerformance:
    """Test UI performance metrics."""
    
    @pytest.mark.skipif("RUN_SELENIUM_TESTS" not in os.environ,
                       reason="UI performance tests require Selenium")
    def test_page_load_times(self, ui_server):
        """Test page load times for different UI pages."""
        # This would require Selenium to properly measure
        # For now, we'll do a simple HTTP check
        pages = [
            "/",  # Dashboard
            "/?page=adrs",
            "/?page=qualities",
            "/?page=risks",
            "/?page=technical_debts",
            "/?page=components",
        ]
        
        results = {}
        
        for page in pages:
            times = []
            for _ in range(5):
                start = time.time()
                response = requests.get(f"{ui_server}{page}")
                end = time.time()
                
                if response.status_code == 200:
                    times.append((end - start) * 1000)
            
            if times:
                results[page] = {
                    "avg": statistics.mean(times),
                    "min": min(times),
                    "max": max(times)
                }
        
        print(f"\nUI Page Load Times:")
        for page, metrics in results.items():
            print(f"{page}: avg={metrics['avg']:.2f}ms, min={metrics['min']:.2f}ms, max={metrics['max']:.2f}ms")
        
        # Basic assertions
        for page, metrics in results.items():
            assert metrics['avg'] < 2000, f"Page load too slow for {page}"
