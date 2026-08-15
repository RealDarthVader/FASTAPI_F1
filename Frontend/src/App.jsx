import React, { useState, useEffect } from 'react';
import './App.css';
import { getSchedule, getDriverResults, getFavorites, addFavorite, deleteFavorite } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('races');
  const [selectedYear, setSelectedYear] = useState(2024);
  const [schedule, setSchedule] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedGp, setSelectedGp] = useState('Monaco');

  
  const currentYear = 2026;
  const availableYears = Array.from(
    { length: currentYear - 1950 + 1 }, 
    (_, i) => currentYear - i
);  

  useEffect(() => {
    fetchScheduleAndFavorites(selectedYear);
  }, [selectedYear]);

  const fetchScheduleAndFavorites = async (year) => {
    try {
      setLoading(true);
      const [schedData, favsData] = await Promise.all([
        getSchedule(year),
        getFavorites(),
      ]);
      setSchedule(schedData);
      setFavorites(favsData);
    } catch (err) {
      console.error("Error fetching schedule:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadDriverResults = async (gp, year = selectedYear) => {
    try {
      setLoading(true);
      setSelectedGp(gp);
      const data = await getDriverResults(year, gp);
      setDrivers(data);
    } catch (err) {
      console.error("Error fetching driver results:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleFavorite = async (driver) => {
    const isFav = favorites.find((f) => f.driver_code === driver.DriverNumber || f.driver_name === driver.BroadcastName);
    try {
      if (isFav) {
        await deleteFavorite(isFav.driver_code);
        setFavorites(favorites.filter((f) => f.id !== isFav.id));
      } else {
        const saved = await addFavorite({
          driver_code: driver.DriverNumber,
          driver_name: driver.BroadcastName,
          team_name: driver.TeamName,
          user_notes: `Saved from ${selectedGp} GP (${selectedYear})`,
        });
        setFavorites([...favorites, saved]);
      }
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="header">
        <div>
          <h1>🏎️ FastF1 Live Dashboard</h1>
          <span className="badge">FastAPI + React</span>
        </div>
        
        {/* Season Selector Dropdown */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
          <label style={{ fontWeight: 600, color: 'var(--text-muted)' }}>Season:</label>
          <select 
            value={selectedYear} 
            onChange={(e) => setSelectedYear(Number(e.target.value))}
            style={{
              backgroundColor: 'var(--card-bg)',
              color: 'var(--text-main)',
              border: '1px solid var(--border-color)',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              fontSize: '1rem',
              cursor: 'pointer'
            }}
          >
            {availableYears.map((yr) => (
              <option key={yr} value={yr}>{yr} Season</option>
            ))}
          </select>
        </div>
      </header>

      <div className="tabs">
        <button
          className={`tab-btn ${activeTab === 'races' ? 'active' : ''}`}
          onClick={() => setActiveTab('races')}
        >
          {selectedYear} Race Calendar
        </button>
        <button
          className={`tab-btn ${activeTab === 'drivers' ? 'active' : ''}`}
          onClick={() => setActiveTab('drivers')}
        >
          Race Results ({selectedGp})
        </button>
        <button
          className={`tab-btn ${activeTab === 'favorites' ? 'active' : ''}`}
          onClick={() => setActiveTab('favorites')}
        >
          Saved Favorites ({favorites.length})
        </button>
      </div>

      {loading && <p>Loading data from FastAPI backend...</p>}

      {activeTab === 'races' && (
        <div className="grid-cards">
          {schedule.map((race) => (
            <div key={race.RoundNumber} className="card">
              <span className="badge">Round {race.RoundNumber}</span>
              <h3>{race.EventName}</h3>
              <p style={{ color: 'var(--text-muted)' }}>📍 {race.Location}, {race.Country}</p>
              <p style={{ fontSize: '0.9rem' }}>📅 {race.EventDate.split(' ')[0]}</p>
              <button
                className="btn-fav"
                onClick={() => {
                  loadDriverResults(race.Location, selectedYear);
                  setActiveTab('drivers');
                }}
              >
                View Results
              </button>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'drivers' && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Pos</th>
                <th>No.</th>
                <th>Driver</th>
                <th>Team</th>
                <th>Points</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {drivers.length === 0 ? (
                <tr><td colSpan="6" style={{ textAlign: 'center' }}>No results loaded yet. Select a race from the calendar!</td></tr>
              ) : (
                drivers.map((d) => (
                  <tr key={d.DriverNumber}>
                    <td><strong>P{d.Position || 'DNF'}</strong></td>
                    <td>{d.DriverNumber}</td>
                    <td>{d.BroadcastName}</td>
                    <td>{d.TeamName}</td>
                    <td>{d.Points}</td>
                    <td>
                      <button
                        className="btn-fav"
                        onClick={() => handleToggleFavorite(d)}
                      >
                        {favorites.some((f) => f.driver_code === d.DriverNumber) ? '★ Favorited' : '☆ Save'}
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'favorites' && (
        <div className="grid-cards">
          {favorites.length === 0 ? (
            <p>No favorites added yet. Go to Results and star a driver!</p>
          ) : (
            favorites.map((fav) => (
              <div key={fav.id} className="card">
                <h3>{fav.driver_name} (#{fav.driver_code})</h3>
                <p style={{ color: 'var(--text-muted)' }}>🏎️ {fav.team_name}</p>
                <p style={{ fontSize: '0.85rem' }}>📝 {fav.user_notes || 'No notes'}</p>
                <button
                  className="btn-fav"
                  style={{ borderColor: '#ef4444', color: '#ef4444' }}
                  onClick={async () => {
                    await deleteFavorite(fav.driver_code);
                    setFavorites(favorites.filter((f) => f.id !== fav.id));
                  }}
                >
                  Remove
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}