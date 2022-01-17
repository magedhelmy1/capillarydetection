import React, {Component} from 'react';
import {Button, Stack} from "react-bootstrap";

class Info extends Component {


    render() {


        return (

            <Stack gap={3} style={{
                position: 'absolute', left: '50%', top: '30%',
                transform: 'translate(-50%, -50%)'
            }}>
                <div className="bg-light border">
                    Contact: Maged Helmy - magedaa@uio.no
                </div>
                <div>
                    <Button>
                        <td onClick={() => window.open("https://github.com/magedhelmy1/capillarydetection",
                            "_blank")}>Github Repo
                        </td>
                    </Button>
                </div>
            </Stack>

        )
    }
}

export default Info;
