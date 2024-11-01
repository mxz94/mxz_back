// src/components/ActivityList.jsx
import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import activities from '/public/activities.json';
import './ActivityList.css';

const ActivityCard = ({ period, summary, monthlyDistances, interval, activityType }) => {
    const generateLabels = () => {
        if (interval === 'year') {
            return Array.from({ length: 12 }, (_, i) => i + 1); // 1 to 12 for months
        } else if (interval === 'month') {
            const [year, month] = period.split('-').map(Number);
            const daysInMonth = new Date(year, month, 0).getDate();
            return Array.from({ length: daysInMonth }, (_, i) => i + 1);
        } else if (interval === 'week') {
            return Array.from({ length: 7 }, (_, i) => i + 1);
        }
        return [];
    };

    const data = generateLabels().map((unit) => ({
        unit,
        distance: monthlyDistances[unit - 1] || 0,
    }));

    const formatTime = (seconds) => {
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = seconds % 60;
        return `${h}h ${m}m ${s}s`;
    };

    const formatPace = (speed) => {
        if (speed === 0) return '0:00';
        const pace = 60 / speed;
        const minutes = Math.floor(pace);
        const seconds = Math.round((pace - minutes) * 60);
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds} min/km`;
    };

    return (
        <div className="activityCard">
            <h2 className="activityName">{period}</h2>
            <div className="activityDetails">
                <p><strong>总距离:</strong> {summary.totalDistance.toFixed(2)} km</p>
                <p><strong>平均速度:</strong> {activityType === 'ride' ? `${summary.averageSpeed.toFixed(2)} km/h` : formatPace(summary.averageSpeed)}</p>
                <p><strong>总时间:</strong> {formatTime(summary.totalTime)}</p>
                {interval !== 'day' && (
                    <>
                        <p><strong>活动次数:</strong> {summary.count}</p>
                        <p><strong>最远距离:</strong> {summary.maxDistance.toFixed(2)} km</p>
                        <p><strong>最快速度:</strong> {activityType === 'ride' ? `${summary.maxSpeed.toFixed(2)} km/h` : formatPace(summary.maxSpeed)}</p>
                    </>
                )}
                {interval === 'day' && (
                    <p><strong>地址:</strong> {summary.location || '未知'}</p>
                )}
                {['month', 'week', 'year'].includes(interval) && (
                    <div className="chart" style={{ height: '250px', width: '100%' }}>
                        <ResponsiveContainer>
                            <BarChart data={data} margin={{ top: 20, right: 20, left: 0, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="unit" />
                                <YAxis label={{ value: 'km', angle: -90, position: 'insideLeft' }} />
                                <Tooltip />
                                <Bar dataKey="distance" fill="#8884d8" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                )}
            </div>
        </div>
    );
};

const ActivityList = () => {
    const [interval, setInterval] = useState('month');
    const [activityType, setActivityType] = useState('run');

    const toggleInterval = (newInterval) => {
        setInterval(newInterval);
    };

    const filterActivities = (activity) => {
        return activity.type.toLowerCase() === activityType;
    };

    const convertTimeToSeconds = (time) => {
        const [hours, minutes, seconds] = time.split(':').map(Number);
        return hours * 3600 + minutes * 60 + seconds;
    };

    const cleanLocation = (location) => {
        return location
            .replace(/\b\d{5,}\b/g, '')
            .replace(/,?\s*(?:\w+省|中国)/g, '')
            .replace(/,+/g, ',')
            .replace(/^,|,$/g, '')
            .trim();
    };

    const groupActivities = (interval) => {
        return activities.filter(filterActivities).reduce((acc, activity) => {
            const date = new Date(activity.start_date);
            let key;
            switch (interval) {
                case 'year':
                    key = date.getFullYear();
                    break;
                case 'month':
                    key = `${date.getFullYear()}-${date.getMonth() + 1}`;
                    break;
                case 'week':
                    const startOfYear = new Date(date.getFullYear(), 0, 1);
                    const weekNumber = Math.ceil(((date - startOfYear) / 86400000 + startOfYear.getDay() + 1) / 7);
                    key = `${date.getFullYear()}-W${weekNumber}`;
                    break;
                case 'day':
                    key = date.toISOString().split('T')[0];
                    break;
                default:
                    key = date.getFullYear();
            }
            if (!acc[key]) acc[key] = { totalDistance: 0, totalTime: 0, count: 0, monthlyDistances: Array(12).fill(0), maxDistance: 0, maxSpeed: 0, location: '' };
            const distanceKm = activity.distance / 1000;
            const speedKmh = distanceKm / (convertTimeToSeconds(activity.moving_time) / 3600);
            acc[key].totalDistance += distanceKm;
            acc[key].totalTime += convertTimeToSeconds(activity.moving_time);
            acc[key].count += 1;
            acc[key].monthlyDistances[date.getMonth()] += distanceKm;
            if (distanceKm > acc[key].maxDistance) acc[key].maxDistance = distanceKm;
            if (speedKmh > acc[key].maxSpeed) acc[key].maxSpeed = speedKmh;
            if (interval === 'day') acc[key].location = cleanLocation(activity.location_country || '未知');
            return acc;
        }, {});
    };

    const activitiesByInterval = groupActivities(interval);

    return (
        <div className="activityList">
            <div className="filterContainer">
                <select onChange={(e) => setActivityType(e.target.value)} value={activityType}>
                    <option value="run">跑步</option>
                    <option value="ride">骑行</option>
                </select>
                <select onChange={(e) => toggleInterval(e.target.value)} value={interval}>
                    <option value="year">按年</option>
                    <option value="month">按月</option>
                    <option value="week">按周</option>
                    <option value="day">按天</option>
                </select>
            </div>
            <div className="summaryContainer">
                {Object.entries(activitiesByInterval).sort(([a], [b]) => b.localeCompare(a)).map(([period, summary]) => (
                    <ActivityCard
                        key={period}
                        period={period}
                        summary={{
                            totalDistance: summary.totalDistance,
                            averageSpeed: summary.totalTime ? (summary.totalDistance / (summary.totalTime / 3600)) : 0,
                            totalTime: summary.totalTime,
                            count: summary.count,
                            maxDistance: summary.maxDistance,
                            maxSpeed: summary.maxSpeed,
                            location: summary.location,
                        }}
                        monthlyDistances={summary.monthlyDistances}
                        interval={interval}
                        activityType={activityType}
                    />
                ))}
            </div>
        </div>
    );
};

export default ActivityList;