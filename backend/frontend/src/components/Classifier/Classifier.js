import React, {Component} from 'react';
import Dropzone from 'react-dropzone';
import './Classifier.css'
import {Spinner, Button, Alert, Image, Container, Row, Col} from 'react-bootstrap'
import axios from 'axios'

const API_URL = process.env.REACT_APP_AXIOS_URL
console.log("ALO: 1301")
console.log("The URL Is")
console.log(`${process.env.REACT_APP_AXIOS_URL}/`)
console.log(API_URL)
console.log("End of the URL Is")

class Classifier extends Component {
    state = {
        files: [],
        isLoading: false,
        recentImage: null,
        dropzone: null,
        sample: null,
        showAnalyzed: true,
        showSegmented: false,
        showOriginal: false,

    }

    show_original = () => {

        this.setState({
            showOriginal: true,
            showAnalyzed: false,
            showSegmented: false
        });
    }

    show_analyzed = () => {

        this.setState({
            showOriginal: false,
            showAnalyzed: true,
            showSegmented: false
        });
    }

    show_segmented = () => {

        this.setState({
            showOriginal: false,
            showAnalyzed: false,
            showSegmented: true
        });
    }

    handleClick = (e) => {

        const prefix = e.target.dataset.prefix;

        const FILES = {
            "image_1": [{
                name: "Sample 1",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`
            }],
            "image_2": [{
                name: "Sample 2",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_3": [{
                name: "Sample 3",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_4": [{
                name: "Sample 4",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_5": [{
                name: "Sample 5",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_6": [{
                name: "Sample 6",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_7": [{
                name: "Sample 7",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_8": [{
                name: "Sample 8",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_9": [{
                name: "Sample 9",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_10": [{
                name: "Sample 10",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_11": [{
                name: "Sample 11",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_12": [{
                name: "Sample 12",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_13": [{
                name: "Sample 13",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_14": [{
                name: "Sample 14",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],

            "image_15": [{
                name: "Sample 15",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_16": [{
                name: "Sample 16",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_17": [{
                name: "Sample 17",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_18": [{
                name: "Sample 18",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_19": [{
                name: "Sample 19",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_20": [{
                name: "Sample 20",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
            "image_21": [{
                name: "Sample 21",
                image: require(`../../static_media/${prefix}.png`).default,
                backend_address: `${prefix}`

            }],
        }

        // you can now use this value to load your images
        this.setState({
            files: [],
            isLoading: true,
            recentImage: null,
            dropzone: null,
            sample: true
        })
        this.loadImage(FILES[`image_${prefix}`])
    }

    onDrop = (files) => {
        this.setState({
            files: [],
            isLoading: true,
            dropzone: true,
            sample: null,
            recentImage: null
        })
        this.loadImage(files)
    }

    loadImage = (files) => {
        setTimeout(() => {
            this.setState({
                files,
                isLoading: false
            }, () => {
                console.log(this.state.files[0])
            })
        }, 1000);
    }

    activateSpinner = () => {
        this.setState({
            files: [],
            isLoading: true,
        })
    }

    deactivateSpinner = () => {
        this.setState({isLoading: false})
    }

    sendImage_dropzone = () => {

        const API_URL = process.env.REACT_APP_AXIOS_URL
        console.log("The URL Is")
        console.log(`${process.env.REACT_APP_AXIOS_URL}/`)
        console.log(API_URL)
        console.log("End of the URL Is")

        this.activateSpinner()
        let formData = new FormData()
        formData.append('picture', this.state.files[0])
        axios.post(`${process.env.REACT_APP_AXIOS_URL}/api/images/`, formData, {
            headers: {
                'accept': 'application/json',
                'content-type': 'multipart/form-data'
            }
        })
            .then(resp => {
                this.getImageClass(resp)
                console.log(resp.data.id)
            })
            .catch(err => {
                console.log(err)
            })
    }

    sendImage_sample = () => {

        const API_URL = process.env.REACT_APP_AXIOS_URL
        console.log("The URL Is")
        console.log(`${process.env.REACT_APP_AXIOS_URL}/`)
        console.log(API_URL)
        console.log("End of the URL Is")


        this.activateSpinner()
        let formData = new FormData()
        formData.append('backend_address', this.state.files[0].backend_address)
        axios.post(`${process.env.REACT_APP_AXIOS_URL}/api/images/`, formData, {
            headers: {
                'accept': 'application/json',
                'content-type': 'multipart/form-data'
            }
        })
            .then(resp => {
                this.getImageClass(resp)
                console.log(resp.data.id)
            })
            .catch(err => {
                console.log(err)
            })
    }

    getImageClass = (obj) => {

        const API_URL = process.env.REACT_APP_AXIOS_URL
        console.log("The URL Is")
        console.log(`${process.env.REACT_APP_AXIOS_URL}/`)
        console.log(API_URL)
        console.log("End of the URL Is")

        axios.get(`${process.env.REACT_APP_AXIOS_URL}/api/images/${obj.data.id}/`,
            {
                headers: {
                    'accept':
                        'application/json',
                }
            },
        )
            .then(resp => {
                this.setState({recentImage: resp})
                console.log("Get image class response is:")
                console.log(resp)
            })
            .catch(err => {
                console.log(err)
            })
        this.deactivateSpinner()

    }


    render() {


        const files = this.state.files.map(file => (
            <li key={file.name}>
                {file.name}
            </li>
        ));
        return (


            <Container>

                <Row>
                    <Col sm={12}>
                        <Dropzone onDrop={this.onDrop} accept='image/png, image/jpeg'>
                            {({isDragActive, getRootProps, getInputProps}) => (
                                <div {...getRootProps({className: 'dropzone back'})}>
                                    <input {...getInputProps()} />
                                    <i className="far fa-image mb-2 text-muted" style={{fontSize: 100}}></i>
                                    <p className='text-muted'>{isDragActive ? "Drop some images " : "Drag 'n' drop some files here, or click to select files"}</p>
                                </div>
                            )}
                        </Dropzone>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <button
                            data-prefix="1"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 1
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="2"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 2
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="3"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 3
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="4"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 4
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="5"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 5
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="6"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 6
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="7"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 7
                        </button>
                    </Col>
                </Row>

                <Row className='mt-1'>
                    <Col sm>
                        <button
                            data-prefix="8"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 8
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="9"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 9
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="10"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 10
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="11"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 11
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="12"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 12
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="13"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 13
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="14"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 14
                        </button>
                    </Col>
                </Row>

                <Row className='mt-1'>
                    <Col sm>
                        <button
                            data-prefix="15"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 15
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="16"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 16
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="17"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 17
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="18"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 18
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="19"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 19
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="20"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 20
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="21"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 21
                        </button>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <div className="mt-2">
                            {
                                this.state.isLoading &&
                                <Spinner animation="border" role="status"></Spinner>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <aside>
                            {files}
                        </aside>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {
                            this.state.recentImage &&
                            <button
                                onClick={this.show_original}
                                className="btn btn-success">
                                Original Image
                            </button>
                        }
                    </Col>
                    <Col sm>
                        {
                            this.state.recentImage &&
                            <button
                                onClick={this.show_analyzed}
                                className="btn btn-success">
                                Analyzed Image
                            </button>
                        }
                    </Col>
                    <Col sm>
                        {
                            this.state.recentImage &&
                            <button
                                onClick={this.show_segmented}
                                className="btn btn-success">
                                Segmented Image
                            </button>
                        }
                    </Col>

                </Row>

                <Row>
                    <Col sm>
                        <div className="img-fluid mt-2">
                            {this.state.files.length > 0 && this.state.dropzone != null &&
                            <Image
                                src={URL.createObjectURL(this.state.files[0])}
                                height='400' rounded/>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <div className="img-fluid">
                            {this.state.files.length > 0 && this.state.sample != null &&
                            <Image
                                src={this.state.files[0].image}
                                height='400' rounded/>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {this.state.recentImage && this.state.showAnalyzed &&
                        <Image className='justify-content-center'
                               src={this.state.recentImage.data.analyzed_picture}
                               height='400' rounded/>

                        }

                        {this.state.recentImage && this.state.showOriginal &&
                        <Image className='justify-content-center'
                               src={this.state.recentImage.data.picture}
                               height='400' rounded/>

                        }

                        {this.state.recentImage && this.state.showSegmented &&
                        <Image className='justify-content-center'
                               src={this.state.recentImage.data.segmented_image}
                               height='400' rounded/>

                        }


                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {this.state.files.length > 0 && this.state.dropzone != null &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage_dropzone}>Analyze
                            Image </Button>}

                        {this.state.files.length > 0 && this.state.sample != null &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage_sample}>Analyze
                            Sample
                            Image </Button>}

                        {
                            this.state.recentImage &&
                            <div className="mt-2">
                                <Alert variant='primary'>
                                    <p> Time Taken: {this.state.recentImage.data.classified} </p>
                                    <p> Number of Capillaries: {this.state.recentImage.data.number_of_capillaries} </p>
                                    <p> Capillary Density : {this.state.recentImage.data.capillary_area} (1 pixel =
                                        2.2µm) </p>

                                </Alert>
                            </div>
                        }
                    </Col>
                </Row>

            </Container>


        )
    }
}

export default Classifier;


