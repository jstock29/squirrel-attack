import * as React from 'react';
import {ActivityIndicator, Button, Card, Checkbox, Headline, Paragraph} from 'react-native-paper';
import {useState} from "react";
import DropDown from "react-native-paper-dropdown";
import {StyleSheet, Text} from "react-native";


const Predictor = () => {
    const [isLoading, setLoading] = useState(false);
    const [showDropDown, setShowDropDown] = useState(false);
    const [pred, setPred] = useState(null);
    const [furColor, setFurColor] = React.useState('Gray');
    const [flags, setFlags] = React.useState(false);
    const [twitches, setTwitches] = React.useState(false);

    const furColorList=[
        {label: 'Gray',value:'Gray'},
        {label: 'Cinnamon',value:'Cinnamon'},
        {label: 'Black',value:'Black'}
    ]


    const predict = async (flags: boolean, twitches: boolean, primary_fur_color: string) => {
        console.log(flags, twitches, primary_fur_color)
        try {
            const response = await fetch(`http://localhost:8000/predict/?flags=${flags}&twitches=${twitches}&primary_fur_color=${primary_fur_color}`,
                {
                    mode: 'cors',
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'}
                });
            const json = await response.json();
            console.log(json.prediction)
            setPred(json.prediction);
            setLoading(false)

        } catch (error) {
            console.error(error);
            setLoading(false)

        } finally {
            setLoading(false);
        }
    }

    return (
        <Card>
            <Card.Title title="Describe your squirrel" subtitle=""/>
            <Card.Cover
                source={{uri: 'https://i.insider.com/6049175c9942cf001865d9ef?width=1136&format=jpeg'}}/>
            <Card.Content>
                <DropDown
                    label={"Fur Color"}
                    mode={"outlined"}
                    visible={showDropDown}

                    showDropDown={() => setShowDropDown(true)}
                    onDismiss={() => setShowDropDown(false)}
                    value={furColor}
                    setValue={setFurColor}
                    list={furColorList}
                />
                <Checkbox.Item
                    status={flags ? 'checked' : 'unchecked'}
                    label={"Flags its tail"}
                    onPress={() => {
                        setFlags(!flags);
                    }}></Checkbox.Item>
                <Checkbox.Item
                    status={twitches ? 'checked' : 'unchecked'}
                    label={"Twitches its tail"}
                    onPress={() => {
                        setTwitches(!twitches);
                    }}></Checkbox.Item>
            </Card.Content>

            <Card.Actions>
                <Button icon="" mode="contained" onPress={() => predict(flags,
                    twitches,
                    furColor,
                )}>Predict</Button>
            </Card.Actions>
            <Card.Content>
                {isLoading &&
                <ActivityIndicator/>
                }
                {pred!==null &&
                <div>
                    <Paragraph>{pred===false
                        ? <Headline style={styles.harmless}>Chill, that squirrel is harmless!</Headline>
                        : <Headline style={styles.scary}>Yep, better get out of there!</Headline>
                    }</Paragraph>
                </div>
                }
            </Card.Content>
        </Card>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        // maxWidth:400,
        // alignItems: 'center',
        // justifyContent: 'center',
    },
    bottom: {
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
    },
    harmless:{
        color:'green',
    },
    scary:{
        color:'red',
    },
});

export default Predictor;
