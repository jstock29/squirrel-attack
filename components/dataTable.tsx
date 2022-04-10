import * as React from 'react';
import {Card, DataTable} from 'react-native-paper';
import {useEffect, useState} from "react";

const optionsPerPage = [10,25,50];

interface squirrelData {
    "Unique Squirrel ID":string;
    "Shift":string;
    "Age":string;
    "Primary Fur Color":string;
    "Location":string;
    "Tail flags":string;
    "Tail twitches":string;
    "Approaches":string;
}

const CustomTable = () => {
    const [isLoading, setLoading] = useState(true);
    const [squirrels, setSquirrels] = useState([]);

    const getSquirrels = async () => {
        try {
            const response = await fetch(`http://localhost:8000/squirrels/`,
                {
                    mode: 'cors',
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'}
                });
            const json = await response.json();
            setSquirrels(json);
            setLoading(false)


        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    }

    const [page, setPage] = React.useState<number>(0);
    const [itemsPerPage, setItemsPerPage] = React.useState(optionsPerPage[0]);

    React.useEffect(() => {
        setPage(0);
    }, [itemsPerPage]);

    useEffect(() => {
        setLoading(true)
        getSquirrels();
    }, []);

    return (
        <Card>
        <DataTable>
            <DataTable.Header>
                <DataTable.Title>Squirrel ID</DataTable.Title>
                <DataTable.Title>Shift</DataTable.Title>
                <DataTable.Title>Age</DataTable.Title>
                <DataTable.Title>Fur Color</DataTable.Title>
                <DataTable.Title>Location</DataTable.Title>
                <DataTable.Title>Tail Flags</DataTable.Title>
                <DataTable.Title>Tail Twitches</DataTable.Title>
                <DataTable.Title>Approaches</DataTable.Title>
            </DataTable.Header>

            { squirrels.map((d: squirrelData) => <DataTable.Row key={d['Unique Squirrel ID']}>
                <DataTable.Cell>{d["Unique Squirrel ID"]}</DataTable.Cell>
                <DataTable.Cell>{d["Shift"]}</DataTable.Cell>
                <DataTable.Cell>{d["Age"]}</DataTable.Cell>
                <DataTable.Cell>{d["Primary Fur Color"]}</DataTable.Cell>
                <DataTable.Cell>{d["Location"]}</DataTable.Cell>
                <DataTable.Cell>{d["Tail flags"].toString()}</DataTable.Cell>
                <DataTable.Cell>{d["Tail twitches"].toString()}</DataTable.Cell>
                <DataTable.Cell>{d["Approaches"].toString()}</DataTable.Cell>
            </DataTable.Row>) }
            <DataTable.Pagination
                page={page}
                numberOfPages={10}
                onPageChange={(page) => setPage(page)}
                label=""
                optionsPerPage={optionsPerPage}
                itemsPerPage={itemsPerPage}
                setItemsPerPage={setItemsPerPage}
                showFastPagination
                optionsLabel={'Rows per page'}
            />
        </DataTable>
        </Card>
    );
}

export default CustomTable;
