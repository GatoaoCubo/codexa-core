"""
Test Suite for Unified CRUD System
Tests all CRUD managers: UnifiedCRUDManager, RepositoryCRUD, DocsCRUD, MLCRUD
"""

import json
import sys
import io
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from shared import (
    UnifiedCRUDManager,
    CRUDStatus,
    RepositoryCRUD,
    DocsCRUD,
    DocType,
    MLCRUD,
    ProcessingStatus
)


def test_unified_crud_base():
    """Test basic UnifiedCRUDManager functionality"""
    print("\n" + "="*80)
    print("TEST 1: UnifiedCRUDManager Base Class")
    print("="*80)

    class TestCRUD(UnifiedCRUDManager):
        """Simple test implementation"""

        def _create_tables(self):
            import sqlite3
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS test_items (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        value TEXT
                    )
                """)
                conn.commit()

        def _get_table_name(self) -> str:
            return "test_items"

    # Initialize
    crud = TestCRUD(db_path="test_unified.db", data_dir="test_data")

    # Test hash functions
    assert len(crud.calculate_hash_md5("test content")) == 12
    assert len(crud.calculate_hash_sha256("test content")) == 64
    print("[✓] Hash functions working")

    # Test audit logging
    crud.log_audit('TEST', 'TEST_001', 'Test audit entry')
    audit = crud.get_audit_log(limit=1)
    assert len(audit) > 0
    assert audit[0]['action'] == 'TEST'
    print("[✓] Audit logging working")

    # Test database info
    db_info = crud.get_database_info()
    assert 'test_items' in db_info['tables']
    assert 'audit_log' in db_info['tables']
    print(f"[✓] Database info: {len(db_info['tables'])} tables")

    # Test statistics
    crud.record_statistic('test_metric', 42.5, {'source': 'test'})
    stats = crud.get_statistics_history('test_metric', limit=1)
    assert len(stats) > 0
    assert stats[0]['metric_value'] == 42.5
    print("[✓] Statistics working")

    # Cleanup
    import time
    import gc
    del crud
    gc.collect()
    time.sleep(0.5)  # Give time for DB to close

    try:
        Path("test_unified.db").unlink(missing_ok=True)
        import shutil
        if Path("test_data/backups").exists():
            shutil.rmtree("test_data/backups")
        if Path("test_data/archived").exists():
            shutil.rmtree("test_data/archived")
        if Path("test_data").exists():
            Path("test_data").rmdir()
    except Exception as e:
        print(f"[!] Cleanup warning: {e}")

    print("\n[✓✓✓] UnifiedCRUDManager base tests PASSED!\n")
    return True


def test_repository_crud():
    """Test RepositoryCRUD functionality"""
    print("\n" + "="*80)
    print("TEST 2: RepositoryCRUD")
    print("="*80)

    # Initialize
    repo = RepositoryCRUD(root_dir=".", db_path="test_repo.db")

    # Test scan (limited to avoid long execution)
    print("\n[*] Scanning repository (this may take a moment)...")
    stats = repo.scan_repository(verbose=False)
    assert stats['total_files'] > 0
    print(f"[✓] Repository scan: {stats['total_files']} files indexed")

    # Test search
    results = repo.search("crud")
    print(f"[✓] Search 'crud': {len(results)} results")

    # Test list by category
    scripts = repo.list_by_category('scripts_processing')
    if scripts:
        print(f"[✓] List by category: {len(scripts)} scripts found")
    else:
        print("[!] No scripts in category (expected if repo is small)")

    # Test LLM export
    export = repo.export_for_llm("test_llm_export.json")
    assert export['total_files'] > 0
    print(f"[✓] LLM export: {export['total_files']} files")

    # Test master index generation
    index = repo.generate_master_index("TEST_REPOSITORY_INDEX.md")
    assert "Repository Master Index" in index
    print("[✓] Master index generated")

    # Test database info
    db_info = repo.get_database_info()
    print(f"[✓] Database: {db_info['database_size_mb']:.2f} MB, {len(db_info['tables'])} tables")

    # Cleanup
    import time
    import gc
    del repo
    gc.collect()
    time.sleep(0.5)

    try:
        Path("test_repo.db").unlink(missing_ok=True)
        Path("test_llm_export.json").unlink(missing_ok=True)
        Path("TEST_REPOSITORY_INDEX.md").unlink(missing_ok=True)
    except Exception as e:
        print(f"[!] Cleanup warning: {e}")

    print("\n[✓✓✓] RepositoryCRUD tests PASSED!\n")
    return True


def test_docs_crud():
    """Test DocsCRUD functionality"""
    print("\n" + "="*80)
    print("TEST 3: DocsCRUD")
    print("="*80)

    # Initialize
    docs = DocsCRUD(docs_dir="test_docs", db_path="test_docs.db")

    # Test CREATE
    test_content = """# Test Document

This is a test document for DocsCRUD.

## Features
- Create, read, update, delete
- Archive and restore
- Search functionality
"""

    success = docs.create("test_doc.md", test_content, {
        'description': 'Test document for CRUD',
        'tags': ['test', 'crud', 'docs'],
        'category': 'testing'
    })
    assert success
    print("[✓] CREATE: Document created")

    # Test READ
    doc = docs.read_by_filename("test_doc.md")
    assert doc is not None
    assert doc['title'] == 'Test Document'
    assert 'test' in doc['tags']
    print(f"[✓] READ: Document '{doc['title']}' retrieved")

    # Test UPDATE
    success = docs.update(doc['id'], metadata={
        'description': 'Updated description',
        'version': '1.1'
    })
    assert success
    updated_doc = docs.read(doc['id'])
    assert updated_doc['version'] == '1.1'
    print("[✓] UPDATE: Document updated")

    # Test SEARCH
    results = docs.search('test')
    assert len(results) > 0
    print(f"[✓] SEARCH: {len(results)} documents found")

    # Test LIST
    all_docs = docs.list_all()
    assert len(all_docs) > 0
    print(f"[✓] LIST: {len(all_docs)} total documents")

    # Test STATISTICS
    stats = docs.get_statistics()
    assert stats['total_documents'] > 0
    print(f"[✓] STATISTICS: {stats['total_documents']} documents, {stats['total_size_mb']} MB")

    # Test ARCHIVE
    success = docs.delete(doc['id'], permanent=False)
    assert success
    archived_doc = docs.read(doc['id'])
    assert archived_doc['status'] == CRUDStatus.ARCHIVED.value
    print("[✓] ARCHIVE: Document archived")

    # Test RESTORE
    success = docs.restore_from_archive(doc['id'])
    assert success
    restored_doc = docs.read(doc['id'])
    assert restored_doc['status'] == CRUDStatus.ACTIVE.value
    print("[✓] RESTORE: Document restored")

    # Test PERMANENT DELETE
    success = docs.delete(doc['id'], permanent=True)
    assert success
    print("[✓] DELETE: Document deleted permanently")

    # Cleanup
    import time
    import gc
    import shutil
    del docs
    gc.collect()
    time.sleep(0.5)

    try:
        Path("test_docs.db").unlink(missing_ok=True)
        if Path("test_docs").exists():
            shutil.rmtree("test_docs")
    except Exception as e:
        print(f"[!] Cleanup warning: {e}")

    print("\n[✓✓✓] DocsCRUD tests PASSED!\n")
    return True


def test_ml_crud():
    """Test MLCRUD functionality"""
    print("\n" + "="*80)
    print("TEST 4: MLCRUD")
    print("="*80)

    # Pre-cleanup any existing test files
    import shutil
    try:
        Path("test_ml.db").unlink(missing_ok=True)
        if Path("test_ml_data").exists():
            shutil.rmtree("test_ml_data")
    except:
        pass

    # Initialize
    ml = MLCRUD(db_path="test_ml.db", data_dir="test_ml_data")

    # Test CREATE
    import hashlib
    test_hash = hashlib.md5(b'test_content_unique').hexdigest()

    test_record = {
        'id': 'TEST_001',
        'source_file': 'RAW/test.md',
        'card_id': 'CARD_ML_test001',
        'domain': 'testing',
        'status': ProcessingStatus.COMPLETED.value,
        'quality_score': 0.85,
        'confidence': 0.78,
        'file_size': 1024,
        'content_hash': test_hash
    }

    success = ml.create(test_record)
    assert success
    print("[✓] CREATE: Processed file created")

    # Test READ
    record = ml.read('TEST_001')
    assert record is not None
    assert record['domain'] == 'testing'
    assert record['quality_score'] == 0.85
    print(f"[✓] READ: Record '{record['id']}' retrieved")

    # Test read by source
    record = ml.read_by_source('RAW/test.md')
    assert record is not None
    print("[✓] READ BY SOURCE: Record found")

    # Test read by card_id
    record = ml.read_by_card_id('CARD_ML_test001')
    assert record is not None
    print("[✓] READ BY CARD_ID: Record found")

    # Test UPDATE
    success = ml.update('TEST_001', {
        'quality_score': 0.90,
        'confidence': 0.85,
        'processing_notes': 'Updated after review'
    })
    assert success
    updated = ml.read('TEST_001')
    assert updated['quality_score'] == 0.90
    print("[✓] UPDATE: Record updated")

    # Test QUALITY METRICS
    ml.record_quality_metric('TEST_001', 'completeness', 0.92)
    ml.record_quality_metric('TEST_001', 'coherence', 0.88)
    metrics = ml.get_quality_metrics('TEST_001')
    assert len(metrics) == 2
    print(f"[✓] QUALITY METRICS: {len(metrics)} metrics recorded")

    # Test BATCH PROCESSING
    batch_id = 'BATCH_TEST_001'
    success = ml.create_batch(batch_id, total_files=10, notes="Test batch")
    assert success
    print("[✓] BATCH CREATE: Batch created")

    ml.update_batch(batch_id, completed=5, failed=1)
    batch_status = ml.get_batch_status(batch_id)
    assert batch_status['completed_files'] == 5
    assert batch_status['failed_files'] == 1
    print(f"[✓] BATCH UPDATE: {batch_status['completed_files']} completed, {batch_status['failed_files']} failed")

    # Test LIST operations
    all_records = ml.list_all()
    assert len(all_records) > 0
    print(f"[✓] LIST ALL: {len(all_records)} records")

    by_domain = ml.list_by_domain('testing')
    assert len(by_domain) > 0
    print(f"[✓] LIST BY DOMAIN: {len(by_domain)} records in 'testing' domain")

    by_quality = ml.list_by_quality(min_quality=0.8, max_quality=1.0)
    assert len(by_quality) > 0
    print(f"[✓] LIST BY QUALITY: {len(by_quality)} high-quality records")

    # Test STATISTICS
    stats = ml.get_statistics()
    assert stats['total_files'] > 0
    print(f"[✓] STATISTICS: {stats['total_files']} files, avg quality: {stats['quality_metrics']['avg_quality']}")

    # Test BULK IMPORT
    bulk_records = [
        {
            'id': f'BULK_{i}',
            'source_file': f'RAW/bulk_{i}.md',
            'card_id': f'CARD_BULK_{i}',
            'domain': 'bulk_test',
            'quality_score': 0.7 + (i * 0.05),
            'confidence': 0.6 + (i * 0.05),
            'content_hash': f'hash_{i}'  # Unique hash for each record
        }
        for i in range(5)
    ]
    imported = ml.bulk_import(bulk_records)
    assert imported == 5
    print(f"[✓] BULK IMPORT: {imported} records imported")

    # Test BULK UPDATE
    bulk_ids = [f'BULK_{i}' for i in range(5)]
    updated = ml.bulk_update_status(bulk_ids, ProcessingStatus.ARCHIVED.value)
    assert updated == 5
    print(f"[✓] BULK UPDATE: {updated} records updated")

    # Test DELETE with backup
    success = ml.delete('TEST_001', backup=True)
    assert success
    deleted = ml.read('TEST_001')
    assert deleted is None
    print("[✓] DELETE: Record deleted with backup")

    # Check backup exists
    backups = ml.list_backups('backup_TEST_001_*.json')
    assert len(backups) > 0
    print(f"[✓] BACKUP: {len(backups)} backup(s) found")

    # Cleanup
    import time
    import gc
    import shutil
    del ml
    gc.collect()
    time.sleep(0.5)

    try:
        Path("test_ml.db").unlink(missing_ok=True)
        if Path("test_ml_data").exists():
            shutil.rmtree("test_ml_data")
    except Exception as e:
        print(f"[!] Cleanup warning: {e}")

    print("\n[✓✓✓] MLCRUD tests PASSED!\n")
    return True


def run_all_tests():
    """Run all test suites"""
    print("\n" + "#"*80)
    print("# UNIFIED CRUD SYSTEM - COMPREHENSIVE TEST SUITE")
    print("#"*80)

    tests = [
        ("UnifiedCRUDManager Base", test_unified_crud_base),
        ("RepositoryCRUD", test_repository_crud),
        ("DocsCRUD", test_docs_crud),
        ("MLCRUD", test_ml_crud),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
            print(f"\n[✗✗✗] {test_name} FAILED: {e}\n")

    # Summary
    print("\n" + "#"*80)
    print("# TEST SUMMARY")
    print("#"*80 + "\n")

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for test_name, success, error in results:
        status = "[✓ PASSED]" if success else "[✗ FAILED]"
        print(f"{status} {test_name}")
        if error:
            print(f"         Error: {error}")

    print(f"\n{'='*80}")
    print(f"TOTAL: {passed}/{total} tests passed")
    print('='*80 + "\n")

    return passed == total


if __name__ == "__main__":
    import sys

    success = run_all_tests()

    if success:
        print("\n[SUCCESS] All tests passed! ✓✓✓")
        sys.exit(0)
    else:
        print("\n[FAILURE] Some tests failed! ✗✗✗")
        sys.exit(1)
