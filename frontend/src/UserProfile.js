const UserProfile = ({ userName, onLogout }) => {
  return (
    <div>
      <h2>Welcome, {userName}!</h2>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
};

export default UserProfile;