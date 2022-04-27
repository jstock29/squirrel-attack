import React, {useEffect, useState} from 'react';
import {StyleSheet, View} from 'react-native';
import {
    Appbar,
    Provider as PaperProvider,

} from 'react-native-paper';
import {StatusBar} from 'expo-status-bar';
import CustomTable from "./components/dataTable";
import Predictor from "./components/predictor";

export default function App() {
    useEffect(() => {
        // setLoading(true)
    }, []);
    const [isLoading, setLoading] = useState(true);

    return (
        <PaperProvider>
            <Appbar.Header>
                <Appbar.Content title="Squirrel Aggression Predictor" subtitle={"They're really not aggressive creatures"} />
            </Appbar.Header>
            <View style={styles.container}>
                <StatusBar style="auto"/>
                <Predictor/>
                <CustomTable/>
            </View>
        </PaperProvider>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        // maxWidth:400,
    },
    bottom: {
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
    }
});
