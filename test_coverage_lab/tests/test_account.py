"""
Test Cases for Account Model
"""
import json
from pathlib import Path
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open(Path(__file__).parent / 'fixtures' / 'account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture
def setup_account():
    """Fixture to create a test account"""
    account = Account(name="John businge", email="john.businge@example.com")
    db.session.add(account)
    db.session.commit()
    return account

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error

# ===========================
# Test: Account Serialization
# Author: Glen Testamark
# Date: 2026-09-14
# Description: Ensure accounts are serialized properly to a dictionary and fields match expected keys.
# ===========================

def test_to_dict():
    acct = Account(name="Nas Jones", email="nas@ill.matic")
    acct_dict = acct.to_dict()
    expected_keys = {
            "id",
            "name",
            "email",
            "phone_number",
            "disabled",
            "date_joined",
            "balance",
            "role"
    }
    # Ensure acct_dict is a dict and the keys match and that test fails
    # for an arbitrary incorrect set of keys 
    assert isinstance(acct_dict, dict)
    assert expected_keys == acct_dict.keys()
    assert acct_dict["name"] == acct.name and acct_dict["email"] == acct.email

# ===========================
# Test: Account Missing Required Fields
# Author: Glen Testamark
# Date: 2026-09-14
# Description: Ensure accounts contain the required name and email fields by
# testing for DataValidationError on accounts without the required fields set.
# ===========================

def test_required_fields():
    # Test default parameter, name only, and email only accounts.
    with pytest.raises(DataValidationError):
        Account().validate_required_fields()
    with pytest.raises(DataValidationError):
        Account(name="foo").validate_required_fields()
    with pytest.raises(DataValidationError):
        Account(email="bar@bar.binks").validate_required_fields()


# ===========================
# Test: Password Hashing
# Author: Michael Podolsky
# Date: 2026-09-09
# Description: Ensure passwords are properly hashed and that password verification works correctly.
# ===========================

def test_password_hashing():
    """Test that passwords are hashed and verified correctly"""
    account = Account(name="Michael Podolsky", email="podolm1@unlv.nevada.edu")
    password = "secret-password"

    account.set_password(password)

    # The password is stored as a hash, not as plaintext
    assert account.password_hash is not None
    assert account.password_hash != password

    # Verification succeeds for the correct password only
    assert account.check_password(password) is True
    assert account.check_password("wrong-password") is False

# ===========================
# Test: Account Deactivation and Reactivation
# Author: Russell Kennedy
# Date: 2026-09-14
# Description: Ensure an active account can be deactivated and reactivated.
# ===========================

def test_account_deactivation_and_reactivation(setup_account):
    """Test deactivating and reactivating an account."""
    assert setup_account.disabled is False

    setup_account.deactivate()
    assert setup_account.disabled is True

    setup_account.reactivate()
    assert setup_account.disabled is False

# ===========================
# Test: Valid Account Withdrawal
# Author: Sokrat Rostomyan
# Date: 2026-09-15
# Description: Ensure a valid withdrawal decreases the account balance.
# ===========================

def test_valid_withdrawal(setup_account):
    """Test withdrawing a valid amount from an account."""
    starting_balance = 100.0
    withdrawal_amount = 30.0
    setup_account.balance = starting_balance

    setup_account.withdraw(withdrawal_amount)

    assert setup_account.balance == pytest.approx(
        starting_balance - withdrawal_amount
    )

# ===========================
# Test: Invalid Email Input
# Author: Peter Nguyen
# Date: 2026-09-16
# Description: Ensure invalid email formats raise a DataValidationError.
# ===========================

def test_invalid_email_input():
    """Test that invalid email formats are rejected"""
    invalid_emails = {
        "fakeemail",
        "noatsign.com",
        "wheredomain@",
        "has spaces.com",
    }
    for bad_email in invalid_emails:
        account = Account(name="Test User", email=bad_email)
        with pytest.raises(DataValidationError):
            account.validate_email()
            
# Test: Positive Account Deposit
# Author: Ethan Guillem
# Date: 2026-09-15
# Description: Ensure a positive deposit increases the balance correctly.
# ===========================

def test_positive_deposit():
    """Test that depositing a positive amount increases the balance."""
    account = Account(
        name="Ethan Guillem",
        email="ethan@example.com",
        balance=100.00,
    )

    account.deposit(50.00)

    assert account.balance == 150.00


# ===========================
# Test: Deleting an account
# Author: Jonathan Johnson
# Date: 2026-09-18
# Description: Ensure an account can be successfull deleted from database. 
# ===========================

def test_delete_account(setup_account):
    """Test that an account can be successfully deleted from database."""
    account = setup_account
    email = account.email
    
    account.delete()
    
    deleted = Account.query.filter_by(email=email).first()
    assert deleted is None
    


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# Test Assignments

# Student 1: Test account serialization -- DONE (Glen Testamark)
# - Verify that the account object is correctly serialized to a dictionary.
# - Ensure all expected fields are included in the output.
# Target Method: to_dict()

# Student 2: Test invalid email input
# - Ensure invalid email formats raise a validation error.
# Target Method: validate_email()

# Student 3: Test missing required fields -- DONE (Glen Testamark)
# - Ensure a DataValidationError is raised when name or email is missing.
# - Note: SQLAlchemy does not validate on construction, so Account() itself
#   never raises. Call the validation method on the constructed object.
# Target Method: validate_required_fields()

# Student 4: Test positive deposit -- DONE (Ethan Guillem)
# - Verify that depositing a positive amount correctly increases the balance.
# Target Method: deposit()

# Student 5: Test deposit with zero/negative values
# - Ensure zero or negative deposits are rejected.
# Target Method: deposit()

# Student 6: Test valid withdrawal
# - Verify that withdrawing a valid amount correctly decreases the balance.
# Target Method: withdraw()

# ===========================
# Test: Test withdrawal with insufficient funds
# Author: Astrid Jimenez
# Date: 2026-09-15
# Description: Ensure withdrawal fails when balance is insufficient
# ===========================

def test_withdraw_insuff_funds():
    """Test withdrawing more than the balance to raise DataValidationError and ensure balance is left unchanged."""
    # Creating sample account
    account = Account(name="Astrid Jimenez", email="jimena29@unv.nevada.edu", balance=50.0)

    # Attempting to withdraw more than balance should raise
    with pytest.raises(DataValidationError):
        account.withdraw(100.0)

    # Failed withdrawal must not alter current balance
    assert account.balance == 50.0


# Student 8: Test password hashing -- DONE (Michael Podolsky)
# - Ensure passwords are properly hashed.
# - Verify that password verification works correctly.
# Target Methods: set_password() / check_password()

# Student 9: Test account deactivation/reactivation
# - Ensure accounts can be deactivated and reactivated correctly.
# Target Methods: deactivate() / reactivate()

# Student 10: Test email uniqueness enforcement
# - Ensure duplicate emails are not allowed.
# Target Method: validate_unique_email()

# Student 11: Test deleting an account -- DONE (Jonathan Johnson)
# - Verify that an account can be successfully deleted from the database.
# Target Method: delete()
