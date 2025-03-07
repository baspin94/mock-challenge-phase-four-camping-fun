import { useEffect, useState } from "react";

function NewSignup({ camperId, onAddActivity }) {
  const [time, setTime] = useState("");
  const [activityId, setActivityId] = useState("");
  const [activities, setActivities] = useState([]);
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    fetch("http://localhost:4000/activities")
      .then((r) => r.json())
      .then(setActivities);
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    const formData = {
      activity_id: Number(activityId),
      camper_id: camperId,
      time: Number(time),
    };
    fetch("http://localhost:4000/signups", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    }).then((r) => {
      if (r.ok) {
        r.json().then((activity) => {
          setTime("");
          setActivityId("");
          setErrors([]);
          onAddActivity(activity);
        });
      } else {
        r.json().then((err) => setErrors(err.errors));
      }
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add New Signup</h2>
      <div>
        <label htmlFor="activity">Activity</label>
        <select
          id="activity"
          value={activityId}
          onChange={(e) => setActivityId(e.target.value)}
        >
          <option value="">Select activity...</option>
          {activities.map((activity) => (
            <option key={activity.id} value={activity.id}>
              {activity.name}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="time">Time</label>
        <input
          type="number"
          id="time"
          value={time}
          onChange={(e) => setTime(e.target.value)}
        />
      </div>
      {errors.map((err) => (
        <p key={err} style={{ color: "red" }}>
          {err}
        </p>
      ))}
      <button type="submit">Submit</button>
    </form>
  );
}

export default NewSignup;
