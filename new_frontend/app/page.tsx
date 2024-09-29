"use client"; // Mark the component as a Client Component

import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import styles from './page.module.css'; // Import CSS module for styling

interface Data {
    time: number[];
    retention: number[];
    slides: string[];
    slide_changes: number[];
}

const Home = () => {
    const [data, setData] = useState<Data | null>(null);
    const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
    const [hoveredLineIndex, setHoveredLineIndex] = useState<number | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('http://localhost:5000/api/data');
            const result: Data = await response.json();
            setData(result);
        };
        fetchData();
    }, []);

    const chartData = {
        labels: data?.time || [],
        datasets: [
            {
                label: 'Retention',
                data: data?.retention || [],
                borderColor: 'rgba(200, 50, 50, 1)', // Change color for Wild West theme
                borderWidth: 2,
                fill: false,
                pointHoverRadius: 5,
            },
        ],
    };

    const options = {
        scales: {
            x: {
                grid: {
                    drawOnChartArea: false,
                },
            },
            y: {
                beginAtZero: true,
            },
        },
        onHover: (event: any, elements: any) => {
            if (elements.length) {
                const index = elements[0].index;
                setHoveredIndex(index);
                setHoveredLineIndex(null);
            } else {
                setHoveredIndex(null);
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: (tooltipItem: any) => {
                        const index = tooltipItem.dataIndex;
                        return `Slide: ${data?.slides[index] || ''}`;
                    },
                },
            },
        },
    };

    const handleMouseMove = (event: React.MouseEvent) => {
        const rect = event.currentTarget.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const totalWidth = rect.width;
        const index = Math.floor((x / totalWidth) * (data?.time.length || 1));

        if (data?.slide_changes.includes(data.time[index])) {
            setHoveredLineIndex(data.time[index]);
        } else {
            setHoveredLineIndex(null);
        }
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Wild West Retention Graph</h1>
            <div className={styles.graphContainer} onMouseMove={handleMouseMove}>
                {data && (
                    <Line
                        data={chartData}
                        options={options}
                    />
                )}
                {data?.slide_changes.map((change) => (
                    <div
                        key={change}
                        style={{
                            position: 'absolute',
                            left: `${((data.time.indexOf(change) / (data.time.length - 1)) * 100)}%`,
                            height: '100%',
                            borderLeft: '2px solid red',
                            top: 0,
                        }}
                    />
                ))}
            </div>
            {(hoveredIndex !== null || hoveredLineIndex !== null) && data && (
                <div className={styles.imagePopup}>
                    <img
                        src={hoveredLineIndex !== null ? data.slides[data.time.indexOf(hoveredLineIndex)] : hoveredIndex !== null ? data.slides[hoveredIndex] : ''}
                        alt="Slide Preview"
                    />
                </div>
            )}
        </div>
    );
};

export default Home;
